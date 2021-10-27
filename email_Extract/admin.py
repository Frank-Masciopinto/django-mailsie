from django.contrib import admin
from . import models
# Register your models here.

# Add a table and chose fields and sorting filter asc desc!

# Add table to be viewed in admin section without fields
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'user']
    list_per_page = 10  # Max records per page

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['placed_at', 'payment_status', 'order_status']
    list_per_page = 10  # Max records per page
# Create a new custom fields to display in admin with your conditions

    @admin.display()
    def order_status(self, order):
        if order.payment_status == 'C':
            return 'OK'
        return 'BAD'
