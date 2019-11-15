import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

from django.contrib.gis.geos import GEOSGeometry
from routepang.model.Location import Location
from routepang.category.LocationCategory import LocationCategory
from routepang.personal import personal

# request에 해당하는 명소(영어명)
# 최대 60개까지 가져옴
# json배열 형태로 return
class LocationController:

    def __init__(self):
        self.google_api_key = personal.mapKey
        self.category = ["attraction", "food", "museum", "grocery", "subwaystation", "church", "hospital", "police"
                         , "lodging", "theater", "bank", "spa"]

    # TODO 카테고리 별로 페이지 넘기지 않 한 페이지 씩만 데이터 추가
    def getLocationList(self, request):

        for category in self.category:
            location_list = []

            # attraction / food / cafe 정도로 category를 나눌 예정
            request_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + request + "+" + \
                            category + "&key=" + self.google_api_key + "&language=ko"

            req = requests.get(request_url)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            # json 형태로 데이터 정제
            json_data = json.loads(str(soup))
            json_loaction_result = json_data["results"]

            location_list = location_list + json_loaction_result

            # try:
            #     next_page_token = json_data["next_page_token"]
            #     # 마지막 페이지에서는
            #     # next_page_token 키가 없기 때문에
            #     # 키에러가 발생
            # except KeyError:
            #     next_page_token = "END"
            #
            # if next_page_token == "END":
            #     break
            # else:
            #         time.sleep(2)

            self.insertLocation(request=location_list)

        return

    # 인스크램 크롤링 목록
    def getLocationNameList(self, request):

        nameList = []

        for i in request:
            # replace를 쓰기 위해 string으로 형변환
            place = str(i["name"])
            nameList.append(place.replace(" ", ""))

        return nameList

    # json 배열을 request
    # json형태의 데이터를 디비에 저장
    def insertLocation(self, request):

        for i in request:
            name = i["name"]

            # location_name으로 중복 검사
            if not Location.objects.filter(name=name).exists():

                place_id = i["place_id"]
                address = i["formatted_address"]
                types = i["types"]

                lon = i["geometry"]["location"]["lng"]
                lat = i["geometry"]["location"]["lat"]
                coordinates = GEOSGeometry('POINT(' + str(lon) + ' ' + str(lat) + ')')

                try:
                    image = i["photos"][0]["photo_reference"]
                except KeyError:
                    image = "no image"

                # 카테고리 해시맵 인스턴스
                c = LocationCategory()
                # 카테고리 넘버
                category = 0
                for type in types:
                    try:
                        category = c.getCategoryNo(type)
                        break
                    # 메인 카테고리에 속하지 않으면 0(UNKNOWN) 처리
                    except KeyError:
                        category = 0

                # print(name, "->", types, "->", category)

                # 카테고리 인스턴스 생성
                # TODO 카테고리에 알맞은 category_number값 추가
                Location(place_id=place_id, address=address, name=name, coordinates=coordinates,
                         image=image, category=category, reg_date=str(datetime.now())[:19],
                         update_date=str(datetime.now())[:19]).save()
            else:
                # 기존의 location은 update_date를 now로 업데이트
                existedLocation = Location.objects.get(name=name)
                existedLocation.update_date = str(datetime.now())[:19]
                existedLocation.save()

        return
