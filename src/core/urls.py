from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserAPIView, RefreshAPIView, \
    LogoutAPIView, UserDetailAPIView

urlpatterns = [
    path('users', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('user', UserAPIView.as_view()),
    path('refresh', RefreshAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('users/<int:id>', UserDetailAPIView.as_view())
]