from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from django.http import JsonResponse

from .models import PlaceDetail
from .serializers import PlacesSerializer, PlaceDetailSerializer
from .fetch_external_api.place_photo import get_place_photos_reference
from concurrent.futures import ThreadPoolExecutor

@api_view()
def get_places(request):
    queryset = PlaceDetail.objects.all()[:20]
    serializer = PlacesSerializer(queryset, many=True)

    serialized_data = list(serializer.data)
    api_key = "AIzaSyApwYVSMh2OxMMrUXJ4CpCSuTA4Noz3U9M"
    max_photos = 3
    place_ids = [data['google_place_id'] for data in serialized_data]

    def fetch_photos(place_id):
        try:
            result = get_place_photos_reference(api_key, place_id, max_photos)
            return result
        except KeyError:
            return None

    with ThreadPoolExecutor() as executor:
        place_photos = list(executor.map(fetch_photos, place_ids))

    for data, photos in zip(serialized_data, place_photos):
        data['place_photo_reference'] = photos

    return Response(serialized_data)







# get a partiular place
@api_view()
def place_detail(request, id):
    place = get_object_or_404(PlaceDetail, pk=id)
    serializer = PlaceDetailSerializer(place)
    return Response(serializer.data)

@api_view()
def place_search(request):
    return Response('ok')