from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
   if created:
      Token.objects.create(user=instance)


class UserProfile(models.Model):
    STATUS_CHOICES = (
        ('T', 'True'),
        ('F', 'False'),
    )
    user = models.OneToOneField(User, related_name='user_profile')
    terms_condition = models.CharField(choices=STATUS_CHOICES, max_length=1)
    activation_key = models.CharField(max_length=40, blank=True ,null=True)
    key_expires = models.DateTimeField(default=now)
    is_alive = models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class Product(models.Model):
    PRODUCT_CATEGORY = (
        ('C', 'Clothes'),
        ('F', 'Food'),
        ('O', 'Office'),
    )
    user = models.ForeignKey(User, related_name="user_id")
    name = models.CharField(max_length=50, unique=False)
    created_date = models.DateTimeField(default=now)
    prod_cat= models.CharField(choices=PRODUCT_CATEGORY, max_length=1)
    cost_of_each = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Cart(models.Model):
    user = models.ForeignKey(User, related_name="user_of_order")
    date_of_order = models.DateTimeField(default=now)
    prod_details = models.ForeignKey(Product,related_name="product_in_order")
    quantity = models.PositiveIntegerField(blank=True, null=True)
    sum_of_prod_cost = models.PositiveIntegerField(blank=True, null=True)

    def add_prod(self,prod_id):
        prod=Product.objects.get(prod_id=prod_id)
        try:
            existing_prod=ProductOrderStatus.objects.get(prod_id=prod_id,order=self)
            existing_prod.quantity_of_each_product +=1
            existing_prod.save()
        except ProductOrderStatus.DoesNotExist:
            create_prod_order=ProductOrderStatus.objects.create(order=self,prod_id=prod_id,quantity_of_each_product=1)
            create_prod_order.save()

    def remove_prod(self,prod_id):
        prod = Product.objects.get(prod_id=prod_id)
        try:
            existing_prod = ProductOrderStatus.objects.get(prod_id=prod_id, order=self)
            if existing_prod.quantity_of_each_product>1:
                existing_prod.quantity_of_each_product -= 1
                existing_prod.save()
        except ProductOrderStatus.DoesNotExist:
            pass

    def __str__(self):
        return str(self.id)


class ProductOrderStatus(models.Model):
    STATUS_ORDER = (
        ('S', 'Start'),
        ('M', 'Payment'),
        ('E', 'Shipped'),
        ('D', 'Delivered'),
        ('P', 'Pending'),
    )

    order = models.ForeignKey(Cart, related_name="Cart_details")
    user = models.ForeignKey(User, related_name="user_of_cart", blank=True, null=True)
    prod=models.ForeignKey(Product,related_name="prod_det")
    quantity_of_each_product= models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(choices=STATUS_ORDER, max_length=1, default='S')


