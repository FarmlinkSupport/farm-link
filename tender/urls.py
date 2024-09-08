from django.urls import path
from .views import TenderListCreateView, TenderRetrieveUpdateDestroyView,TenderGetBuyerView

urlpatterns = [
    path('tenders/', TenderListCreateView.as_view(), name='tender-list-create'),
    path('tenders/<int:id>/', TenderRetrieveUpdateDestroyView.as_view(), name='tender-detail'),
    path('tender/buyer/',TenderGetBuyerView.as_view()),
    
]
