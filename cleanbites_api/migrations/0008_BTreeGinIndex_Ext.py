from django.contrib.postgres.operations import BtreeGinExtension
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('cleanbites_api', '0007_remove_placedetail_search_vector'),
    ]

    operations = [
        BtreeGinExtension(),

    ]

