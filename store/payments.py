import requests
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Payment

User = get_user_model()


def create_paystack_payment(amount, email, order_id):
    user = User.objects.get(email=email)
    if user:
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            'email': email,
            'amount': amount * 100, # Convert amount to kobo
            'callback_url': f"{settings.WEBSITE_DOMAIN}/payment/verify/{order_id}"
        }

        response = requests.post(f'{settings.PAYSTACK_BASE_URL}/transaction/initialize', headers=headers, json=data)
        response_data = response.json()

        if response_data.get('status'):
            # Get paystack generated reference
            paystack_reference = response_data['data']['reference']

            payment = Payment.objects.create(
                user=user,
                amount=amount,
                reference=paystack_reference
            )

            payment_url = response_data['data']['authorization_url']
        return payment_url
    
    return JsonResponse({"error": "Payment initialization failed"}, status=400)



@csrf_exempt
def verify_paystack_payment_view(request, order_id):
    paystack_reference = request.GET.get("reference")

    headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        }
    
    response = requests.get(f"{settings.PAYSTACK_BASE_URL}/transaction/verify/{paystack_reference}", headers=headers)
    response_data = response.json()

    if response_data['data']['status'] == "success":
        payment = Payment.objects.get(reference=paystack_reference)
        payment.status = Payment.COMPLETED
        payment.completed_at = timezone.now()
        payment.save()

        # Send Mail to User with Order details
        order = Order.objects.prefetch_related('order_items__package__package_items__product').get(pk=order_id)
        mail_subject = "Order Details"
        html_message = render_to_string("store/emails/order_detail.html", {
            "order": order,
            "payment": payment
        })

        plain_text = "Order detail"
        email = EmailMultiAlternatives(mail_subject,
                                       plain_text,
                                       settings.EMAIL_HOST_USER,
                                       [request.user.email])
        email.attach_alternative(html_message, 'text/html')
        email.send()
    return JsonResponse({"detail": "It worked"})
    
