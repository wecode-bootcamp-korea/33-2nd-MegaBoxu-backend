from django.urls import path,include

urlpatterns = [
  path('users', include('users.urls')),
  path('movies', include('movies.urls')),
  path('reservations', include('reservations.urls')),
  # path('reviews', include('reviews.urls'))
]
