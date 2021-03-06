# Generated by Django 4.0.4 on 2022-06-12 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_movie_poster_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='age_limit',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='movie',
            name='reservation_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='movie',
            name='total_viewer',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
