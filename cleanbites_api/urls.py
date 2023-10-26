from django.urls import path
# from rest_framework.routers import SimpleRouter
from . import views

# router = SimpleRouter()
# router.register('places')
urlpatterns = [
    # URL pattern for getting a list of places
    path('places/', views.PlacesView.as_view()),

    # URL pattern for fetching a place by ID
    path('places/<int:id>/', views.PlaceDetailView.as_view()),
]
