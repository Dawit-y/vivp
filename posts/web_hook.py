import math
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.views import APIView
import stripe

from accounts.models import Applicant
from posts.models import PaidApplicant, Post

stripe.api_key = settings.STRIPE_SECRET_KEY

class Webhook(APIView):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        payload = request.body
        print(payload)
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        webhook_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload=payload,
                sig_header=sig_header,
                secret=webhook_secret
            )
        except ValueError as e:
            return JsonResponse({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return JsonResponse({'error': 'Invalid signature'}, status=400)

        # Handle the event
        if event['type'] == 'checkout.session.completed':
            session_id = event['data']['object']['id']
            session = stripe.checkout.Session.retrieve(session_id)
            customer_email = session['customer_details']['email']

            try:
                applicant = Applicant.objects.get(email=customer_email)
            except Applicant.DoesNotExist:
                return JsonResponse({'error': 'Applicant not found'}, status=404)

            post_id = session['metadata'].get('post_id')
            if post_id:
                try:
                    post = Post.objects.get(id=post_id)
                except Post.DoesNotExist:
                    return JsonResponse({'error': 'Post not found'}, status=404)
            else:
                return JsonResponse({'error': 'Post ID not found in metadata'}, status=400)
            
            unit_amount = int(math.ceil(post.price * 100))
            if unit_amount != session['amount_total']:
                return JsonResponse({'error': 'Invalid price'}, status=400)

            paid_applicant = PaidApplicant.objects.create(
                post=post,
                applicant=applicant
            )

            print("-----checkout.session.completed----->", customer_email)
        elif event['type'] == 'invoice.paid':
            # Continue to provision the subscription as payments continue to be made.
            # Store the status in your database and check when a user accesses your service.
            # This approach helps you avoid hitting rate limits.
            print("-----invoice.paid----->")
        elif event['type'] == 'invoice.payment_failed':
            # The payment failed or the customer does not have a valid payment method.
            # The subscription becomes past_due. Notify your customer and send them to the
            # customer portal to update their payment information.
            print("-----invoice.payment_failed----->")
        elif event['type'] == 'payment_intent.succeeded':
            # Handle successful payment intents here
            print("-----payment_intent.succeeded----->")
        else:
            print('Unhandled event type')

        return JsonResponse({'success': True})
