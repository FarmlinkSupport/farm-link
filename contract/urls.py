from django.urls import path
from .views import *

urlpatterns = [
    path('delivery/<int:id>/',ContractDeliveryStatusView.as_view()),
    path('contracts/',ContractGetView.as_view()),
    path('decline/<int:id>/',ContractDeclineView.as_view()),
    path('contract_details/<int:id>/',ContractDetails.as_view()),
]
