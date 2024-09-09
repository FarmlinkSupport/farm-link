from django.http import HttpResponse
from rest_framework import response,status,permissions
from .models import Payment
from rest_framework.views import APIView
from accounts.renderers import UserRenderer
import stripe
from django.conf import settings
from tender.models import Tender
from contract.models import Contract
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.core.mail import send_mail
import requests


stripe.api_key=settings.STRIPE_SECRET_KEY

class PaymentCheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        contract_id = self.kwargs['pk']
        try:
            contract = Contract.objects.get(id=contract_id)
            tender = contract.tender

            if request.user != contract.buyer:
                raise PermissionDenied('You are not authorized to access this page!')
            
            if contract.payment_status == 'Pending' or contract.payment_status=='Failed' and contract.status=='Active':
                contract_value_in_cents = int(contract.contract_value * 100)

                checkout_session = stripe.checkout.Session.create(
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'inr',
                                'unit_amount': contract_value_in_cents,
                                'product_data': {
                                    'name': tender.title,
                                    'description': f'{tender.description}  {tender.notice_file}\n'
                                                f'{contract.start_date}\n{contract.end_date}'
                                }
                            },
                            'quantity': 1,
                        },
                    ],
                    metadata={
                        "contract_id": contract.id
                    },
                    mode='payment',
                    success_url=settings.PAYMENT_SITE_URL + f'payment/sucess/{contract.id}/',
                    cancel_url=settings.PAYMENT_SITE_URL + f'payment/cancel/',
                )
                return response.Response({'url': checkout_session.url}, status=status.HTTP_200_OK)
            else:
                return response.Response({'message': 'Buyer has already paid for this contract'},status=status.HTTP_406_NOT_ACCEPTABLE)

        except Contract.DoesNotExist:
            return response.Response({'msg': 'Contract not found'}, status=status.HTTP_404_NOT_FOUND)
        except stripe.error.StripeError as e:
            return response.Response({'msg': 'Stripe error occurred', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return response.Response({'msg': 'An error occurred', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



