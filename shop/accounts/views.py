from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User


from .models import Profile
from items.models import SaleOffer, Item

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }

    return render(request, 'accounts/signup.html', context)


def profile(request, user_id):
    context = {
        'profile': User.objects.get(id=user_id),
        'user': request.user,
        'sales': SaleOffer.objects.filter(item__dealer__id=user_id),
        'items': Item.objects.filter(dealer__id=user_id),
    }

    if request.user.is_authenticated:
        context['cart_items'] = Profile.objects.get(user=request.user).cart_items.all()
    else:
        context['cart_items'] = ['Log in']

    return render(request, 'accounts/profile.html', context)


def cart(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {
        'sales': user_profile.cart_items.all(),
    }

    if request.user.is_authenticated:
        context['cart_items'] = Profile.objects.get(user=request.user).cart_items.all()
    else:
        context['cart_items'] = ['Log in']

    return render(request, 'accounts/cart.html', context)
