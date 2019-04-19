from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserProfile)

admin.site.register(ProductOrderStatus)
admin.site.register(Product)
admin.site.register(Cart)