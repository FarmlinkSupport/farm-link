from django.urls import path
from .views import *

urlpatterns = [
    path('delivery/<int:id>/',ContractDeliveryStatusView.as_view()),
    path('contracts/',ContractGetView.as_view())
]
