from django.urls import path
from . import views

# URLConf
urlpatterns = [path("places/", views.get_places)]