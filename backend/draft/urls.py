from django.urls import path
from .views import DraftCreateListView,DraftUpdateRetrieveDestroyView,DraftStatusUpdateView

urlpatterns = [
    path('drafts/<int:tender_id>/',DraftCreateListView.as_view()),
    path('drafts/<int:id>/',DraftUpdateRetrieveDestroyView.as_view()),
    path('drafts/<int:id>/buyer/',DraftStatusUpdateView.as_view()),
    
]
