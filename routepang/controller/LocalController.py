import requests
from bs4 import BeautifulSoup

import json
import time

def getLocations(request):

    google_api_key = "AIzaSyDsID62DKc24X5B-PpM1daGvv_qGBEJuYU"
    next_page_token = ""
    location_list = []

    # next_page_token이 없을 때까지 넘어가면서 파싱
    while True:
        request_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + request + "+명소&key=" + google_api_key \
                  + "&pagetoken=" + next_page_token + "&language=ko"

        req = requests.get(request_url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        # json 형태로 데이터 정제
        json_data = json.loads(str(soup))
        json_loaction_result = json_data["results"]

        location_list = location_list + json_loaction_result

        try:
            next_page_token = json_data["next_page_token"]
        except KeyError:
            next_page_token = "END"

        if next_page_token == "END":
            break
        else:
            time.sleep(2)

    return location_list