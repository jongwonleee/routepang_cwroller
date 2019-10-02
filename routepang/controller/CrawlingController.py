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

            for i in link_url:
                url_list.append(i.get_attribute('href'))
            pagedowns += 1

        url_list = set(url_list)

        return url_list

    def getInfoFromArticle(request):

         return