# Generated by Django 2.1.7 on 2019-04-12 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_auto_20190412_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='Most_Commented_Posts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='Most_Liked_Posts',
            field=models.IntegerField(default=0),
        ),
    ]
