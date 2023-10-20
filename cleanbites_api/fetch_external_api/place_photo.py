import googlemaps

# define func to get photo reference
def get_place_photos_reference(api_key, place_id, max_photos=5):
    # set api key
    gmaps = googlemaps.Client(key=api_key)
    # parameter(s) to fetch from google api
    required_fields = ['name','photo']

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

