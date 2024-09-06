from django.urls import path
from .views import *

urlpatterns = [
    path('profile/',BuyerProfileView.as_view()),
    path('profile/<int:user__id>/', BuyerProfileDetailView.as_view()),
]
