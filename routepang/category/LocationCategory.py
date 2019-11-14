# TODO ---------- 카테고리 목록 ------------
#               UNKNOWN : 0
#               ATTRACTION : 1
#               FOOD : 2
#               ACTIVITY : 3
#               SHOPPING : 4
#               TRAFFIC : 5
#               RELIGIOUS : 6
#               MEDICAL : 7
#               PUBLIC : 8
#               LODGE : 9
#               ENTERTAINMENT : 10
#               UTILITY : 11
#               SERVICE : 12

class LocationCategory:
    def __init__(self):
        self.category = {
            "accounting" : 0,
            "airport" : 5,
            "amusement_park" : 3,
            "aquarium" : 3,
            "art_gallery" : 3,
            "atm" : 11,
            "bakery" : 2,
            "bank" : 11,
            "bar" : 2,
            "beauty_salon" : 12,
            "bicycle_store" : 4,
            "book_store" : 4,
            "bowling_alley" : 10,
            "bus_station" : 5,
            "cafe" : 2,
            "campground" : 3,
            "car_dealer" : 4,
            "car_rental" : 11,
            "car_repair" : 0,
            "car_wash" : 0,
            "casino" : 10,
            "cemetery" : 0,
            "church" : 6,
            "city_hall" : 8,
            "clothing_store" : 4,
            "convenience_store" : 4,
            "courthouse" : 8,
            "dentist" : 7,
            "department_store" : 4,
            "doctor" : 7,
            "drugstore" : 4,
            "electrician" : 0,
            "electronics_store" : 4,
            "embassy" : 11,
            "fire_station" : 0,
            "florist" : 4,
            "funeral_home" : 0,
            "furniture_store" : 4,
            "gas_station" : 11,
            "grocery_or_supermarket" : 4,
            "gym" : 3,
            "hair_care" : 12,
            "hardware_store" : 4,
            "hindu_temple" : 6,
            "home_goods_store" : 4,
            "hospital" : 7,
            "insurance_agency" : 0,
            "jewelry_store" : 4,
            "laundry" : 11,
            "lawyer" : 0,
            "library" : 1,
            "light_rail_station" : 5,
            "liquor_store" : 4,
            "local_government_office" : 8,
            "locksmith" : 0,
            "lodging" : 9,
            "meal_delivery" : 2,
            "meal_takeaway" : 2,
            "mosque" : 6,
            "movie_rental" : 10,
            "movie_theater" : 10,
            "moving_company" : 0,
            "museum" : 3,
            "night_club" : 10,
            "painter" : 0,
            "park" : 8,
            "parking" : 11,
            "pet_store" : 4,
            "pharmacy" : 7,
            "physiotherapist" : 7,
            "plumber" : 0,
            "police" : 8,
            "post_office" : 8,
            "primary_school" : 0,
            "real_estate_agency" : 0,
            "restaurant" : 2,
            "roofing_contractor" : 0,
            "rv_park" : 3,
            "school" : 0,
            "secondary_school" : 0,
            "shoe_store" : 4,
            "shopping_mall" : 4,
            "spa" : 12,
            "stadium" : 3,
            "storage" : 0,
            "store" : 4,
            "subway_station" : 5,
            "supermarket" : 4,
            "synagogue" : 6,
            "taxi_stand" : 5,
            "tourist_attraction" : 1,
            "train_station" : 5,
            "transit_station" : 5,
            "travel_agency" : 3,
            "university" : 8,
            "veterinary_care" : 7,
            "zoo" : 3
        }

    def getCategoryNo(self, request):
        category_num = self.category[request]

        return category_num