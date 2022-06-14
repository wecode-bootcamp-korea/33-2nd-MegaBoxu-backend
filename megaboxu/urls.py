from django.urls import path,include

urlpatterns = [
  path('user', include('users.urls')),
  path('movie', include('movies.urls')),
  path('reservation', include('reservations.urls')),
  path('review', include('reviews.urls'))

]
