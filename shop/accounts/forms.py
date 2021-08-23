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
    class Meta:
        model = CartMembership
        exclude = ['profile', 'item']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['buyer', 'items', 'status']
