# Generated by Django 3.1.5 on 2021-01-20 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='visits',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
