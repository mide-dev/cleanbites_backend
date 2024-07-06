from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import PlaceDetail, User, UserFavorite, PlaceReview, Category
from .serializers import PlacesSerializer, PlaceDetailSerializer, UserCreateSerializer, UserSerializer, CustomTokenObtainPairSerializer, PlaceReviewSerializer, UserFavoriteSerializer, CategorySerializer
from .permissions import IsAccountOwner
from .fetch_external_api.places_api import enrich_place_detail, get_place_reviews, get_photo_url

import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()
google_api_key = env("GOOGLE_API_KEY")

# USERS VIEWS
class UserView(APIView):
    permission_classes = [IsAuthenticated, IsAccountOwner]

    def get(self, request, id):
        user = get_object_or_404(User, pk=id)
        serializer = UserCreateSerializer(user)
        return Response(serializer.data)

    def put(self, request, id):
        user = get_object_or_404(User, pk=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = get_object_or_404(User, pk=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# PLACE VIEWS
class PlacesView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        queryset = PlaceDetail.objects.all().order_by('?')
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = PlacesSerializer(page, many=True)
        serialized_data = serializer.data
        result = get_photo_url(serialized_data=serialized_data, google_api_key=google_api_key)
        
        return paginator.get_paginated_response(result)


class PlaceSearchView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        search_param = request.GET.get('query')
        vector = SearchVector("category_desc", 'business_name', 'city')
        query = SearchQuery(search_param)
        queryString = search_param
        queryset = PlaceDetail.objects.annotate(search=vector).filter(search=query)

        if len(queryset) < 1:
            queryset = PlaceDetail.objects.annotate(similarity=TrigramSimilarity("business_name", queryString)).filter(similarity__gt=0.4).order_by("-similarity")

        if len(queryset) < 1:
            queryset = PlaceDetail.objects.annotate(similarity=TrigramSimilarity("category_desc", queryString)).filter(similarity__gt=0.1).order_by("-similarity")

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = PlacesSerializer(page, many=True)
        serialized_data = serializer.data

        if len(serializer.data) < 1:
            return Response({'message': "No results available for the search string"}, status=status.HTTP_404_NOT_FOUND)
        result = get_photo_url(serialized_data=serialized_data, google_api_key=google_api_key)
        return paginator.get_paginated_response(result)


class PlaceAutocompleteView(APIView):
    def get(self, request):

        search_string = request.GET.get('query')
        
        categoryQueryset = Category.objects.annotate(similarity=TrigramSimilarity("name", search_string)).filter(similarity__gt=0.15).order_by("-similarity")[:5]
        PlaceQueryset = PlaceDetail.objects.annotate(similarity=TrigramSimilarity("business_name", search_string)).filter(similarity__gt=0.15).order_by("-similarity")[:5]

        categorySerializer = CategorySerializer(categoryQueryset, many=True)
        placeSerializer = PlacesSerializer(PlaceQueryset, many=True)
        serialized_data = {
            'categoriesAutocomplete': categorySerializer.data,
            'placeAutocomplete': placeSerializer.data,
        }

        return Response(serialized_data)


class PlaceDetailView(APIView):
    def get(self, request, place_id):
        place_detail = get_object_or_404(PlaceDetail, pk=place_id)
        serialized = PlaceDetailSerializer(place_detail)
        serialized_data = serialized.data
        google_place_id = serialized_data['google_place_id']
        enriched_data = enrich_place_detail(api_key=google_api_key, place_id=google_place_id)
        serialized_data['google_enriched_data'] = enriched_data
        return Response(serialized_data)
    

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5

class TopPlacesView(APIView):
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        # apply filter
        queryset = PlaceDetail.objects.filter(hygiene_score__gt=4).filter(google_review_score__gt=4).filter(google_review_count__gt=100).order_by('?')
        # paginate & Serialize the results
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = PlacesSerializer(page, many=True)
        serialized_data = serializer.data
        result = get_photo_url(serialized_data=serialized_data, google_api_key=google_api_key)
        
        return paginator.get_paginated_response(result)
    

# PLACE FAVORITES VIEWS
class UserFavoriteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user_favorites = UserFavorite.objects.filter(user=user_id).prefetch_related('place')
        serializer = UserFavoriteSerializer(user_favorites, many=True)
        return Response(serializer.data)

class AddFavoritesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        place_id = request.data.get('place_id')
        place = get_object_or_404(PlaceDetail, pk=place_id)
        user_favorite, created = UserFavorite.objects.get_or_create(user=user, place=place)
        if created:
            return Response({'message': 'Place added to favorites'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Place is already in favorites'}, status=status.HTTP_200_OK)

class RemoveFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, place_id):
        user = request.user
        place = get_object_or_404(PlaceDetail, pk=place_id)
        user_favorite = UserFavorite.objects.filter(user=user, place=place).first()
        if user_favorite:
            user_favorite.delete()
            return Response({'message': 'Place removed from favorites'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Place is not in favorites'}, status=status.HTTP_200_OK)

# REVIEWS VIEWS
class PlaceReviewsListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, place_id):
        reviews = PlaceReview.objects.select_related('user').filter(place_id=place_id)
        serialized_reviews = []

        for review in reviews:
            serialized_review = PlaceReviewSerializer(review).data
            user = review.user
            serialized_review['user_first_name'] = user.first_name
            serialized_review['user_last_name'] = user.last_name
            serialized_reviews.append(serialized_review)

        place_detail = PlaceDetail.objects.values('google_place_id').get(pk=place_id)
        google_place_id = place_detail['google_place_id']

        serialized_data = {'cleanbites_reviews': serialized_reviews}

        if len(serialized_data) >= 5:
            return Response(serialized_data)

        elif len(serialized_data) >= 1:
            google_reviews = get_place_reviews(api_key=google_api_key, place_id=google_place_id)
            serialized_data['google_reviews'] = google_reviews
            return Response(serialized_data)
        else:
            google_reviews = get_place_reviews(api_key=google_api_key, place_id=google_place_id)
            return Response(google_reviews)

class UserReviewsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        reviews = PlaceReview.objects.filter(user_id=user_id)
        serializer = PlaceReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class CreateReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        place_id = request.data.get('place_id')
        review_text = request.data.get('review_text')
        rating = request.data.get('rating')

        place = get_object_or_404(PlaceDetail, pk=place_id)
        google_review_score = place.google_review_score
        google_review_count = place.google_review_count

        # New review count
        new_review_count = google_review_count + 1

        # Get new rating average
        new_rating = ((google_review_count * google_review_score) + rating) / new_review_count
        new_rating = round(new_rating, 2)

        # Update place information
        place.google_review_score = new_rating
        place.google_review_count = new_review_count
        place.save()

        review = PlaceReview.objects.create(user=user, place_id=place, review=review_text, rating=rating)
        serializer = PlaceReviewSerializer(review)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class VerifyIfUserAlreadyReviewed(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        place_id = request.query_params.get('place_id')

        if not place_id:
            return Response({'error': 'Place ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            place = get_object_or_404(PlaceDetail, pk=place_id)
        except ValueError:
            return Response({'error': 'Invalid Place ID format'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user has already left a review for the given place
        review_exists = PlaceReview.objects.filter(user_id=user_id, place_id=place.id).exists()

        if review_exists:
            return Response({'review': 'User has already left a review.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No review found.'}, status=status.HTTP_404_NOT_FOUND)

class EditOrDeleteReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, review_id):
        review = get_object_or_404(PlaceReview, pk=review_id)
        serializer = PlaceReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, review_id):
        review = get_object_or_404(PlaceReview, pk=review_id)
        if review.user == request.user:
            place = review.place_id
            old_rating = review.rating

            review_text = request.data.get('review_text')
            rating = request.data.get('rating')

            review.review = review_text
            review.rating = rating
            review.save()

            # Fetch the place using the place_id to update the rating
            place = get_object_or_404(PlaceDetail, pk=place.id)
            total_ratings = place.google_review_score * place.google_review_count
            total_ratings = total_ratings - old_rating + rating
            place.google_review_score = round(total_ratings / place.google_review_count, 2)
            place.save()

            serializer = PlaceReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You are not allowed to edit this review'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, review_id):
        review = get_object_or_404(PlaceReview, pk=review_id)
        if review.user == request.user:
            place = review.place_id
            rating = review.rating

            review.delete()

            # Fetch the place using the place_id to update the rating and review count
            place = get_object_or_404(PlaceDetail, pk=place.id)
            if place.google_review_count > 1:
                place.google_review_count -= 1
                total_ratings = place.google_review_score * (place.google_review_count + 1)
                total_ratings = total_ratings - rating
                place.google_review_score = round(total_ratings / place.google_review_count, 2)
            else:
                place.google_review_score = 0
                place.google_review_count = 0

            place.save()

            return Response({'message': 'Review deleted'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You are not allowed to delete this review'}, status=status.HTTP_403_FORBIDDEN)