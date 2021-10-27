from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import F, Func, Value
from email_Extract.models import Customer as Customer_x, Order
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from .serializers import CustomerSerializer, OrderSerializer
from email_Extractor.serializers import UserSerializer
from .permissions import IsAdminOrReadOnly
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt # new
from django.conf import settings # new
from django.http.response import JsonResponse, HttpResponse # new
import stripe

# Create your views here.
# Thanks to class you save yourself if, else . statements


class CustomerViewSet(ModelViewSet):
    queryset = Customer_x.objects.all()[:5]
    serializer_class = CustomerSerializer
    lookup_field = "id"
    permission_classes = [IsAdminOrReadOnly]
    # def get_permissions(self):           <<<<<<<<<<<<<<Set Permissions for access on specific methods
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    def get_serializer_context(self):
        return {'request': self.request}

    def delete(self, request, id):
        customer1 = get_object_or_404(Customer_x, pk=id)
        customer1.delete()
        return Response({'Error': 'Customer has been deleted successfully, sire!'}, status=status.HTTP_204_NO_CONTENT)

class FrankViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Customer_x.objects.filter(user__first_name__icontains='frank')
    serializer_class = CustomerSerializer
    #permission_classes = [IsAuthenticated]  <<< to block page for unauthenticated visitors

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        (customer, created) = Customer_x.objects.get_or_create(id=request.user.id)
        if request.method == 'GET':
            serializer = UserSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class Payment(TemplateView):
    template_name = 'payment.html'

#Cross site protection
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

#when button on payment page is clicked will excecute this function to redirect to strip checkout page
@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'emailExtract/success/',
                cancel_url=domain_url + 'emailExtract/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'T-shirt',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '2000',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

#stripe webhoook - Stripe will call this url once a purchase is completed
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        print(event)
        # TODO: run some custom code here

    return HttpResponse(status=200)

class SuccessView(TemplateView):
    template_name = 'pay_success.html'


class CancelledView(TemplateView):
    template_name = 'pay_failed.html'