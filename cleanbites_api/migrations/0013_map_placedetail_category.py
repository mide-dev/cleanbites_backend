from django.db import migrations, models

def map_categories(apps, schema_editor):
    PlaceDetail = apps.get_model('cleanbites_api', 'PlaceDetail')
    Category = apps.get_model('cleanbites_api', 'Category')
    placeCategory = apps.get_model('cleanbites_api', 'placedetail_categories')

    unique_categories = set()
    place_id = 0
    for place in PlaceDetail.objects.all():
        if place.category_desc:
            place_id = place.id
            categories = place.category_desc.split(', ')
            unique_categories.update(categories)

        for category in Category.objects.all():
            if category.name in unique_categories:
                placeCategory.objects.get_or_create(placedetail_id = place_id, category_id= category.id)

        unique_categories.clear()


class Migration(migrations.Migration):

    dependencies = [
        ('cleanbites_api', '0012_join_placedetail_category'),
    ]

    operations = [
        migrations.RunPython(map_categories),
    ]
