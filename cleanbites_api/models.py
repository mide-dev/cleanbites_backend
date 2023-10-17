from django.db import models

# Create your models here.
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


class User(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email = models.EmailField(max_length=254, unique=True)


class UserFavorite(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    place_id = models.ForeignKey(PlaceDetail, on_delete=models.CASCADE)


class PlaceReview(models.Model):
    rating = models.PositiveIntegerField()
    review = models.TextField()
    last_update = models.DateTimeField(auto_now=True)
    place_id = models.ForeignKey(PlaceDetail, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

