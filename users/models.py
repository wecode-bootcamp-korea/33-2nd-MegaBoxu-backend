from django.db import models

from cores.models import TimeStampModel

class User(TimeStampModel):
    kakao_id        = models.CharField(max_length = 45)
    email           = models.CharField(max_length = 45, unique = True)
    name            = models.CharField(max_length = 45)
    phone_number    = models.CharField(max_length = 45)
    point           = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'users'