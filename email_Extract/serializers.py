from django.db.models import fields
from rest_framework import serializers
from .models import Customer, Order, OrderItem
# Converts a product object to dictionary
# Below you choose the fields you want to display to the world and type


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'nick_name']
    nick_name = serializers.SerializerMethodField(method_name='create_nick')

    def create_nick(self, customer: Customer):
        return customer.first_name+' My Sire'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product','quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['placed_at', 'payment_status', 'customer', 'items']