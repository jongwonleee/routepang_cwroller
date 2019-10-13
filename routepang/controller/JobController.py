from routepang.controller.LocalController import LocationController
from routepang.controller.CrawlingController import CrawlingController
from routepang.controller.UrlController import UrlController

from routepang.model.LocationModel import Location
from routepang.model.ArticleModel import Article
from routepang.model.UrlModel import Url


def locationTask():

    location_controller = LocationController()

    # 추후 도시 추가
    location_controller.getLocationList("프랑스+paris")

    return


def urlTask():

    crawling_controller = CrawlingController
    url_controller = UrlController

    # TODO : 도중에 데이터가 들어가는 것을 감안
    nameList = Location.objects.all()

    for location in nameList:
        # -----url을 얼마나 가져울지 판단(100개 정도)----- #
        # 해당 location에 해당하는 게시물들중, 현재 날짜를 기준으로 오래된 게시물들 삭제
        # (삭제한 게시물들 id는 어떻게 관리??)
        # DB에 들어있는 article개수를 판단
        # if 100개 미만) 100개가 되게끔만 긁어옴
        # if 100개 초과) 파싱하지 않음

        # 태그 검색에 불필요한 부분 삭제
        place = str(location.name).replace(" ","").replace("-","").replace("’","").replace(",","")
        urlList = crawling_controller.getAllArticle(place)

        for url in urlList:
            url_controller.insertUrl(url, location.location_id)

    return


def infoTask():

    crawling_controller = CrawlingController
    # TODO : 도중에 데이터가 들어가는 것을 감안
    urlList = Url.objects.all()

    for url in urlList:
        info = crawling_controller.getInfoFromArticle(url)

        crawling_controller.insertArticle(info, url.location_id)

    return