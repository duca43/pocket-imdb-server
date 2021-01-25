# Generated by Django 3.1.5 on 2021-01-25 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0003_movielike'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieWatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watched', models.BooleanField(default=False)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
            ],
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_watch', models.ManyToManyField(through='movies.MovieWatch', to='movies.Movie')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_watch_list', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='moviewatch',
            name='watch_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.watchlist'),
        ),
        migrations.AlterUniqueTogether(
            name='moviewatch',
            unique_together={('movie', 'watch_list')},
        ),
    ]
