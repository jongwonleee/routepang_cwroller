from django.http import HttpResponse
from routepang.controller import LocalController

def home(reqult):

    return HttpResponse("local req")

def getLocationList(request, Nation_name):

    result = LocalController.getLocations(Nation_name)

    # print(result)

    return HttpResponse("correct")