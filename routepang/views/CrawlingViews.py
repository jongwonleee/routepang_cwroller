from django.http import HttpResponse
from routepang.controller.CrawlingController import CrawlingController

def home(reqult):

    return HttpResponse("crawling req")

def getArticle(request, tag):

    CrawlingController.getAllArticle("에펠탑");


    return HttpResponse("correct")