import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from routepang.model.ArticleModel import Article

class CrawlingController:

    # aws에 올린 후 수정 필요
    Driver_Dir = "/Users/cy/PycharmProjects/chromedriver"

    def __init__(self):
        self.driver = webdriver.Chrome(self.Driver_Dir)
        self.driver.implicitly_wait(10)
        self.driver.get("https://www.instagram.com/explore/tags/sample/")
        # 페이지가 인스타 그램인지 확
        assert "Instagram" in self.driver.title

    def __del__(self):
        self.driver.close()

    # 해당 명소에 대한 최신 게시물 url 리스트 return
    def getAllArticle(self, request):
        t = time.time()
        print(t, 'start get all article:')

        # db에 저장할 url의 리스트를 담아 놓을 리스
        url_list = []

        # base_url = "https://www.instagram.com"
        # url = base_url + "/explore/tags/" + request
        # self.driver.get(url)

        elem = self.driver.find_element_by_xpath("//input[@placeholder='검색']")
        # location_name으로 검색창에 검색
        # name에 태그에 들어가면 안되는 문자도 사용 가능
        elem.send_keys(request)

        # 검색 결과 맨 위를 클릭
        try:
            self.driver.find_element_by_css_selector('div.fuqBx > a').click()
        # 검색 결과가 없는 경
        except NoSuchElementException:
            return url_list

        #TODO 검색해서 들어갔는데 location이라서 게시물이 없는 경우

        # body 태그를 태그 이름으로 찾기
        # elem = self.driver.find_element_by_tag_name("body")
        # pagedowns = 1

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        # pagedown수 만큼 스크롤
        while True:
            # for i in range(2):
            #     elem.send_keys(Keys.PAGE_DOWN)

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            print(time.time(), 'pressing pagedown with delay')
            time.sleep(2)

            link_url = self.driver.find_elements_by_css_selector('article.KC1QD > div > div > div > div > a')

            # 해당 게시물에 #{location} 태그가 있는지 확인(보류) #

            for i in link_url:
                # DB에 들어있는 게시에서 중복 확인
                if not Article.objects.filter(url=i).exists():
                    url_list.append(i.get_attribute('href'))
                #TODO 사진 카테고리 확인해서 목적에 맞지 않는 게시물인 경우

            # 가져온 게시물이 50개 이상이면 break
            if len(url_list) >= 50:
                break

            # pagedowns += 1

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            # 스크롤이 더 이상 내려가지 않으면 break
            if new_height == last_height:
                break
            last_height = new_height

        url_list = list(set(url_list))

        print(time.time(), 'elapsed time:', time.time() - t)

        return url_list