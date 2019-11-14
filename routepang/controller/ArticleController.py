import requests
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime

from routepang.model.Article import Article
from routepang.model.Link import Link

class ArticleController:

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
        favicon = soup.find("link", rel="icon")

        summary = summary["content"] if summary else "No Summary"
        image = image["content"] if image else "No Image"
        favicon = "https://www.instagram.com" + str(favicon["href"]) if favicon else "No Fav"

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
        articleInfo.append(favicon)

        print(time.time(), 'end getInfo')

        return articleInfo

    def insertArticle(self, request, locaion_id):

        print(time.time(), 'start insert')

        #TODO 수정 바람
        # 중복검사(url) 추가
        # 이미 링크 테이블에 있는 경우
        if not Link.objects.filter(link_url=request[2]).exists():
            Link(link_url=request[2], favicon_url=request[4], image_url=request[1], summary=request[0]
                 , reg_date=request[3]).save()
            existedLink = Link.objects.get(link_url=request[2])
            Article(location_id=locaion_id, link_id=existedLink.id, image=request[1], summary=request[0]
                    , reg_date=request[3]).save()
        else:
            # 기존의 article은 update_date를 now로 업데이트
            existedLink = Link.objects.get(link_url=request[2])
            existedLink.update_date = str(datetime.now())[:19]
            existedLink.save()
            existedArticle = Article.objects.get(link_id=existedLink.id)
            existedArticle.update_date = str(datetime.now())[:19]
            existedArticle.save()

        print(time.time(), 'end insert')

        return