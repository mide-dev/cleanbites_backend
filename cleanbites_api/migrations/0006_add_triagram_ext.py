from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('cleanbites_api', '0005_placedetail_search_vector'),
    ]

    operations = [
        TrigramExtension(),
    ]