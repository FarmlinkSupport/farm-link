from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path('buyer/<int:pk>/',csrf_exempt(PaymentCheckoutView.as_view()),name="CheckoutSession"),
    path('stripe/webhook/',stripe_webhook_view,name="webhook"),
    
]
