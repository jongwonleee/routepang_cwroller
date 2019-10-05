from django.http import HttpResponse
from routepang.controller.CrawlingController import CrawlingController
from routepang.controller.LocalController import LocationController

def home(reqult):

    return HttpResponse("crawling req")

def getArticle(request, City_name):

    result = LocationController.getLocationList(City_name)
    nameList = LocationController.getLocationNameList(result)

    for i in nameList:
        urlList = CrawlingController.getAllArticle(i)

        for j in urlList:
            info = CrawlingController.getInfoFromArticle(j)

            # laction_id를 db에서 가져와서
            # info와 함께 article 테이블에 save


    return HttpResponse("correct")