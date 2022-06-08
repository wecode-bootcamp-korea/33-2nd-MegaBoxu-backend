from django.db import models
from django.db.models import UniqueConstraint

from cores.models import TimeStampModel

class Review(TimeStampModel):
    user      = models.ForeignKey("users.User", on_delete=models.CASCADE)
    movie     = models.ForeignKey("movies.Movie", on_delete=models.CASCADE)
    content   = models.TextField()
    rating    = models.DecimalField(max_digits=5, decimal_places=2)
    image_url = models.URLField(max_length=600)

    class Meta:
        db_table    = 'reviews'
        constraints = [
            UniqueConstraint(fields = ['user', 'movie'], name='unique_review')
        ]
        
class ReviewLike(models.Model):
    user   = models.ForeignKey("users.User", on_delete=models.CASCADE)
    review = models.ForeignKey("reviews.Review", on_delete=models.CASCADE)

    class Meta:
        db_table = 'review_likes'