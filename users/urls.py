from django.urls import path

from users.views import KakaoLoginView

urlpatterns = [
    path('/kakao/callback', KakaoLoginView.as_view()),
]
