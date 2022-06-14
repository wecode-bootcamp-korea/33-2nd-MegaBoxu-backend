from django.urls import path

from .views import MovieReviewView

urlpatterns = [
    path('/<int:movie_id>', MovieReviewView.as_view())
]