from django.urls import path
from .views import *

urlpatterns = [
    path('profile/',FarmerProfileView.as_view()),
    path('profile/<int:user__id>/', FarmerProfileDetailView.as_view()),
]
