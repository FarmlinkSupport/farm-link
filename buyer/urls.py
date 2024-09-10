from django.urls import path
from .views import *

urlpatterns = [
    path('profile/',BuyerProfileView.as_view()),
    path('profile/<int:user_id>/', BuyerProfileDetailView.as_view()),
    path('buyer/contract/',BuyerContractView.as_view()),
    
]
