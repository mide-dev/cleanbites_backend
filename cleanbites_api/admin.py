from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models

# Register your models here.

@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    ordering = ('email', ('first_name'))
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide"),
                "fields": ("password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )


@admin.register(models.PlaceDetail)
class PlaceDetailAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'hygiene_score']
    list_per_page = 25
    search_fields = ['business_name']


admin.site.register(models.UserFavorite)
admin.site.register(models.PlaceReview)

