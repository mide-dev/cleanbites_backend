from django.db import migrations

def create_categories(apps, schema_editor):
    PlaceDetail = apps.get_model('cleanbites_api', 'PlaceDetail')
    Category = apps.get_model('cleanbites_api', 'Category')

    unique_categories = set()
    for place in PlaceDetail.objects.all():
        if place.category_desc:
            categories = place.category_desc.split(', ')
            unique_categories.update(categories)

    for category_name in unique_categories:
        Category.objects.get_or_create(name=category_name)

class Migration(migrations.Migration):

    dependencies = [
        ('cleanbites_api', '0010_category'),
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]
