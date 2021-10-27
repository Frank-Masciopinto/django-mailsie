from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
# Create your models here.


class Customer(models.Model):
    MEMBERSHIP_DEFAULT = 'F'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_DEFAULT, 'Free'),
        ('M', 'Monthly'),
        ('Q', 'Quaterly'),
        ('Y', 'Yearly'),
    ]
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_DEFAULT)
    # Change Default String Rappresentation of python Object
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.first_name

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    # Create a filter for sorting table by chosen field a-z
    class Meta:
        ordering = ['membership']


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Complete'),
        ('F', 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_CHOICES, default='P')
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.payment_status


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

class Product(models.Model):
    MEMBERSHIP_DEFAULT = 'F'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_DEFAULT, 'Free'),
        ('M', 'Monthly'),
        ('Q', 'Quaterly'),
        ('Y', 'Yearly'),
    ]

    membership_type = models
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_DEFAULT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
