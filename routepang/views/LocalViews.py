from django.http import HttpResponse
from routepang.controller.LocalController import LocationController

def home(reqult):

    return HttpResponse("local req")

def getLocation(request, City_name):

    result = LocationController.getLocationList(City_name)
    LocationController.getLocationNameList(result)
    LocationController.insertLocation(result)

    return HttpResponse("correct")