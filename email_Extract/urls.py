from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register("hello", views.CustomerViewSet)
router.register("new", views.CustomerViewSet)
router.register("frank", views.FrankViewSet)
router.register("orders", views.OrderViewSet)

urlpatterns = [
    path('payment/', views.Payment.as_view(), name='payment'),
    path('config/', views.stripe_config), 
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.SuccessView.as_view()), 
    path('cancelled/', views.CancelledView.as_view()), 
    path('stripe-hook/', views.stripe_webhook), 
]

urlpatterns += router.urls
