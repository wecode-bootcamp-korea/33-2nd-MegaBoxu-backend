from django.urls import path, include

urlpatterns = [
    path('movie', include('movies.urls'))
]