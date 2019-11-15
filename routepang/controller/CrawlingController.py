import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from routepang.model.Link import Link
from routepang.personal import personal

class CrawlingController:

    # aws에 올린 후 수정 필요
    Driver_Dir = "/Users/cy/PycharmProjects/chromedriver"

    def __init__(self):
        # instagram 계정 (개인)
        self.usrId = personal.usrId
        self.pwd = personal.password

        self.driver = webdriver.Chrome(self.Driver_Dir)
        self.driver.implicitly_wait(10)

        # ------- Instagram Login -------- #
        self.driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        elem = self.driver.find_element_by_xpath("//input[@name='username']")
        elem.send_keys(self.usrId)
        elem = self.driver.find_element_by_xpath("//input[@name='password']")
        elem.send_keys(self.pwd)
        self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[4]/button").click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[2]").click()

        # 페이지가 인스타그램인지 확인
        assert "Instagram" in self.driver.title

    def __del__(self):
        self.driver.close()

    # 해당 명소에 대한 최신 게시물 url 리스트 return
    def getAllArticle(self, request):
        time.sleep(2)
        t = time.time()
        print(t, 'start get all article:')

        # db에 저장할 url의 리스트를 담아 놓을 리스트
        url_list = []
        link_url = []

        self.driver.find_element_by_xpath("//input[@placeholder='검색']").clear()
        elem = self.driver.find_element_by_xpath("//input[@placeholder='검색']")
        # location_name으로 검색창에 검색
        # name에 태그에 들어가면 안되는 문자도 사용 가능
        elem.send_keys(request)

        time.sleep(2)
        # 검색 결과 맨 위를 클릭
        try:
            self.driver.find_element_by_css_selector('div.fuqBx > a').click()
        # 검색 결과가 없는 경우 체크
        except NoSuchElementException:
            return url_list
        # 검색한 페이지가 로딩될 때 까지 대기
        time.sleep(5)

        # select page type
        cur_url = str(self.driver.current_url).split('/')
        if len(cur_url) > 4:
            urlType = cur_url[4]
        else:
            urlType = "page"

        print(t, request, '-> start')

        page = self.driver.find_element_by_tag_name("body")
        pagedown = 1
        # 스크롤 하면서 article url 크롤링
        # 최대 50번 스크롤
        while pagedown < 10:
            for i in range(4):
                page.send_keys(Keys.PAGE_DOWN)

            print(time.time(), 'pressing pagedown with delay')
            time.sleep(1)

            # Search by Tag
            if urlType == "tags":
                article_url = self.driver.find_elements_by_css_selector('article.KC1QD > div > div > div > div > a')
                for i in article_url:
                    link_url.append(i)
                # Not enough Recent Article
                # 인기 게시물까지 추가하고 리턴
                if len(article_url) < 12:
                    popular_link = self.driver.find_elements_by_css_selector('article.KC1QD > div.EZdmt > div > div > div > div > a')
                    for link in popular_link:
                        article_url.append(link)
                    url_list = self.getArticleUrl(article_url)
                    return url_list
            # Search by Location
            elif urlType == "locations":
                article_url = self.driver.find_elements_by_css_selector('article.vY_QD > div > div > div > div > a')
                for i in article_url:
                    link_url.append(i)
            # Search by Page
            elif urlType == "page":
                article_url = self.driver.find_elements_by_css_selector('article.FyNDV > div > div > div > div > a')
                for i in article_url:
                    link_url.append(i)

            # 게시물이 없으면
            if len(link_url) == 0:
                return url_list

            # 해당 게시물에 #{location} 태그가 있는지 확인(보류) #

            url_list = self.getArticleUrl(link_url)

            # 가져온 게시물이 20개 이상이면 break
            print('length of Url List:', len(url_list))
            if len(url_list) >= 20:
                break

            pagedown += 1

        print(time.time(), 'elapsed time:', time.time() - t)

        # url_list중에서 앞에 10개만 return
        if len(url_list) > 5:
            return url_list[:5]
        else:
            return url_list

    def getArticleUrl(self, link_url):
        url_list = []

        for i in link_url:
            # DB에 들어있는 article data 중복 확인
            if not Link.objects.filter(link_url=i).exists():
                url_list.append(i.get_attribute('href'))
            # TODO 사진 카테고리 확인해서 목적에 맞지 않는 게시물인 경우
        # 중복 url 제거
        url_list = list(set(url_list))

        return url_list