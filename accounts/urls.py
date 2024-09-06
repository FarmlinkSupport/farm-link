from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView
)
from .views import *

urlpatterns = [
    path('signup/',UserRegistrationView.as_view()),
    path('login/',UserLoginView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
