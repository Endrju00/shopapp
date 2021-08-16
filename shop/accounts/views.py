from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm

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


def profile(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
            'sales': SaleOffer.objects.filter(item__dealer=request.user),
            'items': Item.objects.filter(dealer=request.user),
        }

    return render(request, 'accounts/profile.html', context)
