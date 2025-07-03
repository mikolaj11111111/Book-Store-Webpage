from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#Create Order Item Inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

#Extend Order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_of_order', 'date_shipped']
    fields = ['user', 'full_name', 'email', 'shipping_adress', 'amout_to_pay', 'date_of_order', 'shipped', 'date_shipped']
    inlines = [OrderItemInline]


admin.site.unregister(Order)

admin.site.register(Order, OrderAdmin)