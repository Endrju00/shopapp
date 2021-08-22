from django.contrib import admin
from .models import Profile, CartMembership, Order

# Register your models here.
admin.site.register(Profile)
admin.site.register(CartMembership)
admin.site.register(Order)
