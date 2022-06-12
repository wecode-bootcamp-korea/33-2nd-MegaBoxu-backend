from django.db import models

class Movie(models.Model):
    title            = models.CharField(max_length=100)
    poster_url       = models.URLField(max_length=600)
    description      = models.TextField()
    reservation_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_viewer     = models.PositiveIntegerField(default=0)
    age_limit        = models.CharField(max_length=45)
    release_date     = models.DateField()
    running_time     = models.TimeField()

    class Meta:
        db_table = 'movies'

class MovieLike(models.Model):
    user  = models.ForeignKey("users.User", on_delete=models.CASCADE)
    movie = models.ForeignKey("movies.Movie", on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie_likes'

class DailyViewer(models.Model):
    movie = models.ForeignKey("movies.Movie", on_delete=models.CASCADE)
    date  = models.DateField()
    count = models.PositiveIntegerField()

    class Meta:
        db_table = 'daily_viewers'