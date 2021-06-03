from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Client_type(models.Model):
    class Meta:
        verbose_name = _("Client_type")
        verbose_name_plural = _("Client_types")

    name = models.CharField(_('type_name'),help_text="Client Type Name", max_length=50)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Client_type_detail", kwargs={"pk": self.pk})


class Clients(models.Model):
    name = models.CharField(_('client_name'),max_length=100)
    gst_no = models.CharField(_('client_gst'),max_length=20,blank=True,null=True)
    address = models.TextField(_('address'),blank=True,null=True)
    type_name = models.ForeignKey(Client_type,on_delete=models.DO_NOTHING,
                                    max_length=20, blank=True, null=True,
                                     related_name='client_type')
    balance = models.FloatField(_('balance'),help_text='Balance need to be paid',default=0)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("Client", kwargs={"pk": self.pk})


class Product(models.Model):
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    product_name = models.CharField(_('product_name'),help_text='Products',max_length=20)
    product_quantity = models.IntegerField(_('ML'),help_text='Product Quantity in ML')
    product_cost = models.FloatField(_('cost'),help_text='Actual making Cost per piece')
    product_transport_cost = models.FloatField(_('transport_cost'),help_text='Transport Cost per piece')
    product_pack_cost = models.FloatField(_('packing_cost'),help_text='Packing cost per piece')

    product_total_cost = models.FloatField(_('total_cost'),help_text='Product actual cost+transport+packing',blank=True,null=True)

    total_product_batch = models.IntegerField(_('total_product_batch'),help_text='Total product made on this batch no',blank=True,null=True)
    product_on_batch_sold = models.IntegerField(_('product_sold'),default=0,blank=True,null=True,help_text='When sold addin diff will be product left')
    product_selling_cost = models.FloatField(_('selling_cost'),help_text='Selling Price per piece')
    product_batch_no = models.CharField(_('Batch No'),max_length=20)
    product_status = models.BooleanField(_('Status'),help_text='If product with batch is still in sell 1 YES 0 NO')

    def save(self,*args, **kwargs):
        self.product_total_cost = self.product_cost + self.product_transport_cost + self.product_pack_cost
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})



class Order(models.Model):
    
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


    order_quantity = models.IntegerField(_('quantity'),default=0,help_text='Order Quantity per product')
    product = models.ForeignKey(Product,name='product',
                                    on_delete=models.DO_NOTHING,
                                    limit_choices_to={'product_status':True})
    order_product_cost = models.FloatField(_('product_cost'),help_text='Product cost on total order quantity',
                                                blank=True,null=True)
    order_product_selling = models.FloatField(_('product_selling'),help_text='Product selling price on totak order quantity', 
                                                blank=True,null=True)
    order_by_client = models.ForeignKey(Clients,name='client', on_delete=models.DO_NOTHING)
    date_of_purchase = models.DateTimeField(name='purchase_date',default=timezone.now)
    tax = models.FloatField('Tax percentage',default=12)
    order_taxed_amount = models.FloatField(_('taxed_amount'),blank=True,null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.order_product_cost = self.product.product_total_cost * self.order_quantity
            self.order_product_selling = self.product.product_selling_cost * self.order_quantity
            self.order_taxed_amount = self.order_product_selling + (self.tax * self.order_product_selling / 100)
            self.client.balance += self.order_taxed_amount 
            self.product.product_on_batch_sold += self.order_quantity 
            self.product.save()
            self.client.save()
            super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.product_name

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})


class Payments(models.Model):
    client = models.ForeignKey(Clients,on_delete=models.DO_NOTHING)
    amount_paid = models.FloatField(_('amount_paid'))

    def save(self,*args, **kwargs):
        self.client.balance -= self.amount_paid
        self.client.save()
        super(Payments, self).save(*args, **kwargs)

