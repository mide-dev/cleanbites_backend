from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # AUTH
    path("token/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # USER
    path('users/<int:id>/', views.UserView.as_view()),
    
    # PLACES
    path('places/', views.PlacesView.as_view()),
    path('places/search/<str:search_param>', views.PlaceSearchView.as_view()),
    path('places/<int:place_id>/', views.PlaceDetailView.as_view()),
    
    # USER FAVORITES
    path('users/<int:user_id>/favorites/', views.UserFavoriteListView.as_view()),
    path('users/favorites/add/', views.AddFavoritesView.as_view()),
    path('users/favorites/remove/<int:place_id>/', views.RemoveFavoriteView.as_view()),
    
    # PLACE REVIEWS
    path('places/<int:place_id>/reviews/', views.PlaceReviewsListView.as_view()),
    
    # USER REVIEWS
    path('users/<int:user_id>/reviews/', views.UserReviewsListView.as_view()),
    
    # CREATE AND EDIT REVIEWS
    path('reviews/add/', views.CreateReviewView.as_view()),
    path('reviews/edit-delete/<int:review_id>/', views.EditOrDeleteReviewView.as_view()),
]

