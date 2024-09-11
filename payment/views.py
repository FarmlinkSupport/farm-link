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
                    success_url=settings.PAYMENT_SITE_URL + f'sucess/{contract.id}/',
                    cancel_url=settings.PAYMENT_SITE_URL + f'cancel/{contract.id}/',
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



import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_KEY
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        id = session["metadata"].get("contract_id")

        try:
            contract = Contract.objects.get(id=id)
        except Contract.DoesNotExist:
            logger.error(f"Contract with ID {id} not found")
            return HttpResponse("Contract not found", status=404)

        contract.payment_status = "Buyer Paid"
        contract.save()

        try:
            payment = Payment.objects.create(
                contract=contract,
                payment_intent_id=session.get("payment_intent"),
                payment_method_type=session.get('payment_method_types', [])[0]
            )
            payment.save()
        except Exception as e:
            logger.error(f"Error saving payment: {e}")
            return HttpResponse("Error saving payment", status=500)

        try:
            send_mail(
                subject="Contract Payment Successful",
                message=f"Dear {contract.buyer.name},\n\n"
                        f"Thank you for your payment. Your contract (ID: {contract.contract_id}) has been successfully deployed.\n"
                        f"Contract Value: ₹{contract.contract_value}\n\n"
                        f"We appreciate your trust and business.\n\n"
                        f"Best regards,\n"
                        f"FarmLink Team",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[customer_email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return HttpResponse("Error sending email", status=500)

    return HttpResponse(status=200)
