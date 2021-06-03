from django.contrib import admin
from django import forms
# Register your models here.
from .models import *

class Client_type_admin(admin.ModelAdmin):
    list_display = ('pk','name')

class Clients_admin(admin.ModelAdmin):
    list_display = ('pk','name','gst_no','address','type_name')

class Product_admin(admin.ModelAdmin):
    list_display =  ('pk','product_name','product_quantity',
                'product_cost','product_transport_cost',
                'product_pack_cost','product_total_cost',
                'product_selling_cost','product_batch_no','product_status')

class AddOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('order_quantity',
                        'order_product','client',
                        'purchase_date')

                
class Order_admin(admin.ModelAdmin):
    add_form = AddOrderForm
    exclude = ('orders_product_cost','orders_product_selling')

    list_display = ('pk','order_quantity',
                        'order_product','order_product_cost',
                         'order_product_selling', 'client','purchase_date')

admin.site.register(Client_type,Client_type_admin)
admin.site.register(Clients,Clients_admin)
admin.site.register(Product,Product_admin)
admin.site.register(Order,Order_admin)