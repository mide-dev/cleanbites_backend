# Generated by Django 4.2.6 on 2023-10-31 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cleanbites_api', '0002_alter_placedetail_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='placedetail',
            options={},
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
