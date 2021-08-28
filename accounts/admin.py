from django.contrib import admin
from .models import Profile, CartMembership, Order, OrderMembership, Notification, Mark

# Register your models here.
admin.site.register(Profile)
admin.site.register(CartMembership)
admin.site.register(Order)
admin.site.register(OrderMembership)
admin.site.register(Notification)
admin.site.register(Mark)
