from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .models import PlaceDetail
from .serializers import PlacesSerializer, PlaceDetailSerializer
from .fetch_external_api.place_photo import get_place_photos_reference
from concurrent.futures import ThreadPoolExecutor

import environ
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

# class UserView(CreateModelMixin, )

class PlacesView(APIView):
    def get(self, request):
        queryset = PlaceDetail.objects.all()[:3]
        # serialize queryset    
        serializer = PlacesSerializer(queryset, many=True)
        # store serialized data as list
        serialized_data = list(serializer.data)

        '''
        fetch photo reference of each place from google
        and add to json payload
        '''
        # declare constants
        api_key = env("GOOGLE_API_KEY")
        max_photos = 3
        # extract place_ids of fetched places and store in list
        place_ids = [data['google_place_id'] for data in serialized_data]

        def fetch_photos(place_id):
            try: # try to fetch photo reference of a place
                result = get_place_photos_reference(api_key, place_id, max_photos)
                return result
            except KeyError: # if no photo available, return Null
                return None

        # fetch multiple photo ref at once to speed up performance
        with ThreadPoolExecutor() as executor:
            place_photos = list(executor.map(fetch_photos, place_ids))

        # zip the results into a tuple and append photo ref to serialized data
        for data, photos in zip(serialized_data, place_photos):
            data['place_photo_reference'] = photos

        return Response(serialized_data)


class PlaceDetailView(APIView):
    def get(self, request, id):
        place = get_object_or_404(PlaceDetail, pk=id)
        serializer = PlaceDetailSerializer(place)
        return Response(serializer.data)
    

@api_view()
def place_search(request):
    return Response('ok')