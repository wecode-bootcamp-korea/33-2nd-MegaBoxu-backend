from datetime import datetime, timedelta

from django.db import models

from cores.models import TimeStampModel

class Region(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'regions'

class Theater(models.Model):
    name   = models.CharField(max_length=45)
    region = models.ForeignKey("reservations.Region", on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'theaters'

class MovieTheater(models.Model):
    movie      = models.ForeignKey("movies.Movie", on_delete=models.CASCADE)
    theater    = models.ForeignKey("reservations.Theater", on_delete=models.CASCADE)
    start_time = models.DateTimeField()

    class Meta:
        db_table = 'movie_theaters'

    @property
    def end_time(self):
        start_time   = self.start_time
        running_time = self.movie.running_time
        
        return datetime.strftime(start_time + timedelta(hours=running_time.hour, minutes=running_time.minute), "%H:%M")

class Reservation(TimeStampModel):
    user           = models.ForeignKey("users.User", on_delete=models.CASCADE)
    movie_theather = models.ForeignKey("reservations.MovieTheater", on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'reservations'