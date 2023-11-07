from django.db import migrations, models
# import cleanbites_api

class Migration(migrations.Migration):

    dependencies = [
        ('cleanbites_api', '0011_populate_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='placedetail',
            name='categories',
            field=models.ManyToManyField(to='cleanbites_api.Category'),
        ),
    ]
