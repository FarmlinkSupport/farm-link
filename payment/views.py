from django.http import HttpResponse
from rest_framework import response, status, permissions
from .models import Payment
from rest_framework.views import APIView
from accounts.renderers import UserRenderer
import stripe
from django.conf import settings
from tender.models import Tender
from contract.models import Contract
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
import requests
from asgiref.sync import sync_to_async

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentCheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    async def post(self, request, *args, **kwargs):
        contract_id = self.kwargs['pk']
        try:
            contract = await sync_to_async(Contract.objects.get)(id=contract_id)
            tender = contract.tender

            if request.user != contract.buyer:
                raise PermissionDenied('You are not authorized to access this page!')
            
            if contract.payment_status in ['Pending', 'Failed'] and contract.status == 'Active':
                contract_value_in_cents = int(contract.contract_value * 100)

                checkout_session = await sync_to_async(stripe.checkout.Session.create)(
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'inr',
                                'unit_amount': contract_value_in_cents,
                                'product_data': {
                                    'name': tender.title,
                                    'description': f'{tender.description} {tender.notice_file}\n'
                                                f'{contract.start_date}\n{contract.end_date}'
                                }
                            },
                            'quantity': 1,
                        },
                    ],
                    metadata={"contract_id": contract.id},
                    mode='payment',
                    success_url=settings.PAYMENT_SITE_URL + f'payment/success/{contract.id}/',
                    cancel_url=settings.PAYMENT_SITE_URL + f'payment/cancel/',
                )
                return response.Response({'url': checkout_session.url}, status=status.HTTP_200_OK)
            else:
                return response.Response({'message': 'Buyer has already paid for this contract'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except Contract.DoesNotExist:
            return response.Response({'msg': 'Contract not found'}, status=status.HTTP_404_NOT_FOUND)
        except stripe.error.StripeError as e:
            return response.Response({'msg': 'Stripe error occurred', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return response.Response({'msg': 'An error occurred', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentSuccessStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    async def get(self, request, *args, **kwargs):
        contract_id = self.kwargs['pk']
        try:
            contract = await sync_to_async(Contract.objects.get)(id=contract_id)

            if request.user != contract.buyer:
                raise PermissionDenied('You are not authorized to mark this payment as successful!')

            contract.payment_status = 'Buyer Paid'
            await sync_to_async(contract.save)()

            buyer_email = contract.buyer.email
            contract_value = contract.contract_value
            contract_id = contract.id

            # Use sync_to_async to send email in async view
            await sync_to_async(send_mail)(
                subject="Contract Payment Successful",
                message=f"Dear {contract.buyer.name},\n\n"
                        f"Thank you for your payment. Your contract (ID: {contract_id}) has been successfully deployed.\n"
                        f"Contract Value: ₹{contract_value}\n\n"
                        f"We appreciate your trust and business.\n\n"
                        f"Best regards,\n"
                        f"FarmLink Team",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[buyer_email],
                fail_silently=False,
            )
            response = await sync_to_async(requests.get)(f'https://farmlinkbc.onrender.com/paymentsuccess/{contract_id}/')
            print(response.json())

            return response.Response({'message': 'Payment marked as successful, and confirmation email sent!'}, status=status.HTTP_200_OK)

        except Contract.DoesNotExist:
            return response.Response({'msg': 'Contract not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response({'msg': 'An error occurred', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentFailedStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    async def get(self, request, *args, **kwargs):
        contract_id = self.kwargs['pk']
        try:
            contract = await sync_to_async(Contract.objects.get)(id=contract_id)

            if request.user != contract.buyer:
                raise PermissionDenied('You are not authorized to mark this payment as failed!')

            contract.payment_status = 'Failed'
            await sync_to_async(contract.save)()

            buyer_email = contract.buyer.email
            contract_value = contract.contract_value
            contract_id = contract.id

            # Use sync_to_async to send email in async view
            await sync_to_async(send_mail)(
                subject="Contract Payment Failed",
                message=f"Dear {contract.buyer.name},\n\n"
                        f"Your payment for contract (ID: {contract_id}) has failed.\n"
                        f"Contract Value: ₹{contract_value}\n\n"
                        f"Please try again to make payment.\n\n"
                        f"Best regards,\n"
                        f"FarmLink Team",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[buyer_email],
                fail_silently=True,
            )

            return response.Response({'message': 'Payment marked as failed, and confirmation email sent!'}, status=status.HTTP_200_OK)

        except Contract.DoesNotExist:
            return response.Response({'msg': 'Contract not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response({'msg': 'An error occurred', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
