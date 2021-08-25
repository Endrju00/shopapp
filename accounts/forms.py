from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import CartMembership, Order, OrderMembership


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class CartForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CartForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].label = ""


    class Meta:
        model = CartMembership
        exclude = ['profile', 'cart_item']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['buyer', 'order_items', 'status']
