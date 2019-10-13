import requests
import json
import  time
from bs4 import BeautifulSoup
from datetime import  datetime

from konlpy.tag import Twitter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from routepang.model.ArticleModel import Article

class CrawlingController:

    Driver_Dir = "/Users/cy/PycharmProjects/chromedriver"

    def __init__(self):
        self.driver = webdriver.Chrome(self.Driver_Dir)
        self.driver.implicitly_wait(10)

    # 해당 명소에 대한 최신 게시물 url 리스트 return
    def getAllArticle(self, request):
        t = time.time()
        print(t, 'start get all article:')
        base_url = "https://www.instagram.com"

        url = base_url + "/explore/tags/" + request

        self.driver.get(url)
        # 총 게시물 수를 클래스 이름으로 찾기
        # totalCount = driver.find_element_by_class_name('g47SY').text
        # print("총 게시물:", totalCount)

        # body 태그를 태그 이름으로 찾기
        elem = self.driver.find_element_by_tag_name("body")
        url_list = []

        pagedowns = 1

        # pagedown수 만큼 스크롤
        while pagedowns < 5:
            for i in range(2):
                elem.send_keys(Keys.PAGE_DOWN)
            print(time.time(), 'pressing pagedown with delay')
            time.sleep(0.5)

            link_url = self.driver.find_elements_by_css_selector('article.KC1QD > div > div > div > div > a')

            # 해당 게시물에 #{location} 태그가 있는지 확인
            # 게시물이 100개 이상이 되면 컷
            # if) 게시물이 100개 안되고 더이상 게시물이 없으면 무한루프?

            for i in link_url:
                url_list.append(i.get_attribute('href'))
            pagedowns += 1

        url_list = list(set(url_list))

        print(time.time(), 'elapsed time:', time.time() - t)

        return url_list

    # 해당 url의 게시물의 정보 추출 후
    # summary, image, favicon 순서의 배열 리턴
    def getInfoFromArticle(self, request):

        print(time.time(), 'start getInfo')
        req = requests.get(request)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        articleInfo = []

        summary = soup.find("meta", property="og:title")
        image = soup.find("meta", property="og:image")
        # favicon = soup.find("link", rel="icon")

        summary = summary["content"] if summary else "No Summary"
        image = image["content"] if image else "No Image"
        # favicon = "https://www.instagram.com" + str(favicon["href"]) if favicon else "No Fav"

        articleInfo.append(summary)
        articleInfo.append(image)
        articleInfo.append(request)

        try:
            data = json.loads(soup.find('script', type='application/ld+json').text)
            reg_date = str(data['uploadDate']).replace("T", " ")
        # 등록 시간이 되있지 않으면
        # 크롤링하는 현재 시간으로 등록
        except AttributeError:
            reg_date = str(datetime.now())[:19]

        articleInfo.append(reg_date)

        print(time.time(), 'end getInfo')

        return articleInfo

    def insertArticle(self, request, locaion_id):

        print(time.time(), 'start insert')

        # 중복검사(url) 추가
        if not Article.objects.filter(url=request[2]).exists():
            Article(location_id=locaion_id, image=request[1], summary=request[0], reg_date=request[3]
                   , url=request[2]).save()

        print(time.time(), 'end inert')

        return