from django.urls import path

from .views import RegionTheaterListView, MovieTheaterView

urlpatterns = [
    path('', MovieTheaterView.as_view()),
    path('/region-theater', RegionTheaterListView.as_view())    
]