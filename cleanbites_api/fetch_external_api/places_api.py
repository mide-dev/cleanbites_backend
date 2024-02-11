import googlemaps
from rest_framework.response import Response
from concurrent.futures import ThreadPoolExecutor
from functools import partial
# define func to get photo reference
def get_place_photos_reference(api_key, place_id, max_photos=5):
    # Initialize Google Maps client
    gmaps = googlemaps.Client(key=api_key)

    # Parameters to fetch from Google API
    required_fields = ['photo']

    try:
        # Call the Google Maps API
        response = gmaps.place(place_id=place_id, fields=required_fields)
        photos = response.get('result', {}).get('photos', [])
        
        # Return photo references
        return [photo["photo_reference"] for photo in photos[:max_photos]]
    except Exception as e:
        return None



def construct_photo_url(place_id, google_api_key, maxwidth=600, max_photos=2):
    base_url = "https://maps.googleapis.com/maps/api/place/photo"
    img_refs = get_place_photos_reference(google_api_key, place_id, max_photos)

    # Handle case where no image references were found
    if img_refs is None:
        return None

    # Construct photo URLs
    return [f"{base_url}?maxwidth={maxwidth}&photoreference={img}&key={google_api_key}" for img in img_refs]

    
# 
def get_photo_url(serialized_data, google_api_key, maxwidth=600):
    # Extract place_ids and prepare arguments for threading
    place_ids = [data['google_place_id'] for data in serialized_data]
    args = ((place_id, google_api_key, maxwidth) for place_id in place_ids)

    partial_construct_photo_url = partial(construct_photo_url, google_api_key=google_api_key, maxwidth=maxwidth)
    # Fetch photo URLs in parallel
    with ThreadPoolExecutor() as executor:
        # place_photos = list(executor.map(lambda place_arguments: construct_photo_url(*place_arguments), args))
        place_photos = list(executor.map(partial_construct_photo_url, place_ids))

    # Append photo URLs to the serialized data
    for data, photos in zip(serialized_data, place_photos):
        if photos is not None:
            data['photo_url'] = photos
        else:
            continue

    return serialized_data


# get place details
def enrich_place_detail(api_key, place_id):
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
    place_offers = {offer: place_data.get(offer, False) for offer in required_fields}

    # Handling the extraction of opening_hours to manage when it's missing
    opening_hours = place_data.get('opening_hours', {})
    opening_times = opening_hours.get('weekday_text', [])
    open_now = opening_hours.get('open_now', 'Not Available')

    # Handling formatted_phone_number with a default empty string
    phone_number = place_data.get('formatted_phone_number', 'Not Available')

    # get maximum of 5 photo references
    photo_url = construct_photo_url(place_id=place_id, google_api_key=api_key, maxwidth=1300, max_photos=5)
    photo_url = photo_url if photo_url is not None else []

    # return the cleaned data as an obj
    formatted_data = {
        "opening_times": opening_times,
        "open_now": open_now,
        "phone_number": phone_number,
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
    