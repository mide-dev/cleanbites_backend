from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import GinIndex
from django.conf import settings
from .utils import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['password', 'first_name', 'last_name']
    objects = UserManager()


class PlaceDetail(models.Model):
    business_name = models.CharField(max_length=255)
    category_desc = models.TextField()
    hygiene_score = models.SmallIntegerField()
    google_review_score = models.FloatField(null=True)
    google_review_count = models.PositiveIntegerField()
    google_place_id = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    post_code = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        indexes = [GinIndex(name='searchPlaceIdx', fields=['category_desc', 'business_name', 'city'])]

    def __str__(self) -> str:
        return self.business_name



class UserFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.ForeignKey(PlaceDetail, on_delete=models.CASCADE)


class PlaceReview(models.Model):
    rating = models.PositiveIntegerField()
    review = models.TextField()
    last_update = models.DateTimeField(auto_now=True)
    place_id = models.ForeignKey(PlaceDetail, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

