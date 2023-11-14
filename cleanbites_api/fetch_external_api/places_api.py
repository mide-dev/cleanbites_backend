import googlemaps
from rest_framework.response import Response
from concurrent.futures import ThreadPoolExecutor

# define func to get photo reference
def get_place_photos_reference(api_key, place_id, max_photos=5):
    # set api key
    gmaps = googlemaps.Client(key=api_key)
    # parameter(s) to fetch from google api
    required_fields = ['photo']
    # call the api
    get_photo_reference = gmaps.place(place_id=place_id, fields=required_fields)
    # define list to append fetch results
    place_photo_reference = []
    # loop through result and append to photo_reference list
    for idx, img in enumerate(get_photo_reference['result']['photos']):
        if idx >= max_photos:
            break
        place_photo_reference.append(img["photo_reference"])
    
    return place_photo_reference

# 
def get_photo_url(serialized_data, google_api_key, maxwidth = 600):
    # fetch photo reference of each place from google
    # and add to json payload
    # '''
    # # extract place_ids of fetched places and store in list
    place_ids = [data['google_place_id'] for data in serialized_data]
    def fetch_photos(place_id):
        # constant
        base_url = "https://maps.googleapis.com/maps/api/place/photo"
        try:
            img_ref = get_place_photos_reference(google_api_key, place_id, max_photos=2)
            photo_url = []
            for img in img_ref:
                photo_url.append(f"{base_url}?maxwidth={maxwidth}&photoreference={img}&key={google_api_key}")
            return photo_url
        except KeyError:
            return None
        
    # fetch multiple photo_url at once to speed up performance
    with ThreadPoolExecutor() as executor:
        place_photos = list(executor.map(fetch_photos, place_ids))

    # zip the results into a tuple and append photo ref to serialized data
    for data, photos in zip(serialized_data, place_photos):
        data['photo_url'] = photos
    return (serialized_data)


# get place details
def enrich_place_detail(api_key, place_id, add_reviews=False):
    # set api key
    gmaps = googlemaps.Client(key=api_key)
    # parameter(s) to fetch from google api 
    required_fields = ['wheelchair_accessible_entrance', 'opening_hours',
                       'formatted_phone_number','delivery', 'dine_in', 'price_level', 'reservable', 
                       'serves_beer', 'serves_breakfast','serves_brunch', 'serves_dinner', 
                       'serves_lunch', 'serves_vegetarian_food', 'takeout']
    # call the api
    get_places_data = gmaps.place(place_id=place_id, fields=required_fields)
    # save api results
    place_data = get_places_data['result']
    # extract place offers and format properly
    place_offers = {}
    for offer in ['wheelchair_accessible_entrance', 'delivery', 
                  'dine_in', 'price_level', 'reservable', 'serves_beer',
                  'serves_breakfast', 'serves_brunch', 'serves_dinner',
                  'serves_lunch', 'serves_vegetarian_food', 'takeout']:
        place_offers[offer] = place_data.get(offer, False)
    # get maximum of 5 photo references
    photo_url = get_place_photos_reference(api_key=api_key, place_id=place_id, max_photos=5)
    # return the cleaned data as an obj
    formatted_data = {
        "opening_times": place_data['opening_hours']['weekday_text'],
        "open_now": place_data['opening_hours']['open_now'],
        "phone_number": place_data['formatted_phone_number'],
        "place_offers": place_offers,
        "photo_urls": photo_url
    }
    return formatted_data


# get place reviews
def get_place_reviews(api_key, place_id):
    # set api key
    gmaps = googlemaps.Client(key=api_key)
    # parameter(s) to fetch from google api 
    required_fields = ['reviews']
    # call the api
    get_reviews = gmaps.place(place_id=place_id, fields=required_fields)
    return get_reviews['result']
    