from django.http import HttpResponse
from routepang.controller.CrawlingController import CrawlingController
from routepang.controller.LocalController import LocationController
from routepang.model.LocationModel import Location

def home(reqult):

    return HttpResponse("crawling req")

def getArticle(request, City_name):

    result = LocationController.getLocationList(City_name)
    # -----result에서 이미 DB에 존재하는 location은 저장하지 않음----- <해결> #
    LocationController.insertLocation(result)

    # -----nameList는 DB에서 locaion_name에 부합하는 데이터를 긁어와 구성(공백이 없어야 함)----- #
    # DB에서 Location의 Name만 배열의 형태로 한번에 받아옴
    nameList = Location.objects.all()

    for i in nameList:
        # -----url을 얼마나 가져울지 판단(100개 정도)----- #
        # 해당 location에 해당하는 게시물들중, 현재 날짜를 기준으로 오래된 게시물들 삭제
        # (삭제한 게시물들 id는 어떻게 관리??)
        # DB에 들어있는 article개수를 판단
        # if 100개 미만) 100개가 되게끔만 긁어옴
        # if 100개 초과) 파싱하지 않음

        # 태그 검색에 불필요한 부분 삭
        place = str(i).replace(" ","").replace("-","").replace("’","").replace(",","")

        urlList = CrawlingController.getAllArticle(place)

        for j in urlList:
            info = CrawlingController.getInfoFromArticle(j)

            # laction_id를 db에서 가져와서
            # info와 함께 article 테이블에 save


    return HttpResponse("correct")