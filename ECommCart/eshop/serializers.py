from eshop.models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
   class Meta:
       model = User
       fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')


class UserProfileSerializer(serializers.Serializer):
    user = UserSerializer()
    terms_condition = serializers.CharField(max_length=10,allow_blank=True)
    activation_key = serializers.CharField(max_length=50, allow_blank=True)
    key_expires = serializers.CharField(max_length=50, allow_blank=True)
    is_alive = serializers.BooleanField()
    is_admin = serializers.BooleanField()


class ProductSerializer(serializers.Serializer):
    user = UserSerializer()
    name = serializers.CharField(max_length=50)
    created_date = serializers.DateTimeField(default=now)
    prod_cat = serializers.CharField(max_length=1)
    cost_of_each = serializers.IntegerField(allow_null=True)



class CartSerializer(serializers.Serializer):
    class Meta:
        model = Cart
    user = UserSerializer()
    date_of_order = serializers.DateTimeField(default=now)
    prod_details = ProductSerializer()
    quantity = serializers.IntegerField()
    sum_of_prod_cost = serializers.IntegerField()