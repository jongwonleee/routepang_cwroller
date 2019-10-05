import requests
import json
import  time
from bs4 import BeautifulSoup

from konlpy.tag import Twitter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class CrawlingController:
    # 해당 명소에 대한 최신 게시물 url 리스트 return
    def getAllArticle(request):

        base_url = "https://www.instagram.com"

        url = base_url + "/explore/tags/" + request
        Driver_Dir = "/Users/cy/PycharmProjects/chromedriver"

        driver = webdriver.Chrome(Driver_Dir)
        driver.implicitly_wait(5)

        driver.get(url)
        # 총 게시물 수를 클래스 이름으로 찾기
        # totalCount = driver.find_element_by_class_name('g47SY').text
        # print("총 게시물:", totalCount)

        # body 태그를 태그 이름으로 찾기
        elem = driver.find_element_by_tag_name("body")
        url_list = []

        pagedowns = 1

        while pagedowns < 20:
            for i in range(3):
                elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

            link_url = driver.find_elements_by_css_selector('article.KC1QD > div > div > div > div > a')

            # 해당 게시물에 #{location} 태그가 있는지 확인
            # 게시물이 100개 이상이 되면 컷
            # if) 게시물이 100개 안되고 더이상 게시물이 없으면 무한루프?

            for i in link_url:
                url_list.append(i.get_attribute('href'))
            pagedowns += 1

        url_list = list(set(url_list))

        return url_list

    # 해당 url의 게시물의 정보 추출 후
    # summary, image, favicon 순서의 배열 리턴
    def getInfoFromArticle(request):

        req = requests.get(request)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        articleInfo = []

        summary = soup.find("meta", property="og:title")
        image = soup.find("meta", property="og:image")
        favicon = soup.find("link", rel="icon")

        summary = summary["content"] if summary else "No Summary"
        image = image["content"] if image else "No Image"
        favicon = "https://www.instagram.com" + str(favicon["href"]) if favicon else "No Fav"

        articleInfo.append(summary)
        articleInfo.append(image)
        articleInfo.append(favicon)

        for i in articleInfo:
            print(i)

        return articleInfo