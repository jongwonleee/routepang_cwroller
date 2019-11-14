import requests
import json
import time
from bs4 import BeautifulSoup
from datetime import datetime

from django.contrib.gis.geos import GEOSGeometry
from routepang.model.Location import Location

# request에 해당하는 명소(영어명)
# 최대 60개까지 가져옴
# json배열 형태로 return
class LocationController:

    def __init__(self):
        self.google_api_key = "AIzaSyDsID62DKc24X5B-PpM1daGvv_qGBEJuYU"
        # TODO 카테고리 분류 추가
        self.category = ["attraction", "food", "museum", "grocery", "subway_station", "church", "hospital", "police"
                         , "lodging", "movie_theater", "bank", "spa"]

    # TODO 카테고리 별로 페이지 넘기고 한 페이지 씩만 데이터 추가
    def getLocationList(self, request):

        for i in range(3):
            location_list = []
            next_page_token = ""

            # next_page_token이 없을 때까지 넘어가면서 파싱
            while True:
                # attraction / food / cafe 정도로 category를 나눌 예정
                request_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + request + "+" + \
                              self.category[i] + "&key=" + self.google_api_key + "&pagetoken=" + next_page_token + \
                              "&language=ko"

                req = requests.get(request_url)
                html = req.text
                soup = BeautifulSoup(html, 'html.parser')

                # json 형태로 데이터 정제
                json_data = json.loads(str(soup))
                json_loaction_result = json_data["results"]

                location_list = location_list + json_loaction_result

                try:
                    next_page_token = json_data["next_page_token"]
                    # 마지막 페이지에서는
                    # next_page_token 키가 없기 때문에
                    # 키에러가 발생
                except KeyError:
                    next_page_token = "END"

                if next_page_token == "END":
                    break
                else:
                    time.sleep(2)

            category_number = 0
            if i == 2:
                category_number = i
            else:
                category_number = i+1

            self.insertLocation(request=location_list, category=category_number)

            # for i in location_list:
            #     print(i)

        return

    # 인스크램 크롤링 목록
    # 태그 검색을 위해 공백 X
    def getLocationNameList(self, request):

        nameList = []

        for i in request:
            # replace를 쓰기 위해 string으로 형변환
            place = str(i["name"])
            nameList.append(place.replace(" ", ""))

        return nameList

    # json 배열을 request
    # json형태의 데이터를 디비에 저장
    def insertLocation(self, request, category):

        for i in request:
            name = i["name"]

            # location_name으로 중복 검사
            if not Location.objects.filter(name=name).exists():

                place_id = i["place_id"]
                address = i["formatted_address"]

                lon = i["geometry"]["location"]["lng"]
                lat = i["geometry"]["location"]["lat"]
                coordinates = GEOSGeometry('POINT(' + str(lon) + ' ' + str(lat) + ')')

                try:
                    image = i["photos"][0]["photo_reference"]
                except KeyError:
                    image = "no image"

                Location(place_id=place_id, address=address, name=name, coordinates=coordinates,
                         image=image, category=category).save()
            else:
                # 기존의 location은 update_date를 now로 업데이트
                existedLocation = Location.objects.get(name=name)
                existedLocation.update_date = str(datetime.now())[:19]
                existedLocation.save()

        return
