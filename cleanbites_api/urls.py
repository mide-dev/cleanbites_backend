from django.urls import path
from . import views

# URLConf
urlpatterns = [path("places/", views.get_places),
               path('places/<int:id>/', views.place_detail)]