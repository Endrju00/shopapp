from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Profile, CartMembership, OrderMembership
from .forms import CartForm, OrderForm
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
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CartForm(request.POST)
            if form.is_valid():
                if request.POST.get("delete_item"):
                    item = Item.objects.get(id=request.POST.get("delete_item"))
                    item.delete()
                elif request.POST.get("delete_sale"):
                    sale = SaleOffer.objects.get(id=request.POST.get("delete_sale"))
                    sale.delete()
    else:
        form = CartForm()

    context = {
        'profile': User.objects.get(id=user_id),
        'user': request.user,
        'sales': SaleOffer.objects.filter(item__dealer__id=user_id),
        'items': Item.objects.filter(dealer__id=user_id),
        'form': form
    }

    if request.user.is_authenticated:
        context['cart_items'] = Profile.objects.get(user=request.user).cart_items.all()

    return render(request, 'accounts/profile.html', context)


@login_required
def cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:

            # Deletion
            if request.POST.get('delete'):
                profile = Profile.objects.get(user=request.user)
                sale = SaleOffer.objects.get(id=request.POST.get('delete'))
                item = CartMembership.objects.get(profile=profile, item=sale)
                item.delete()

            # Submit order
            if request.POST.get('submit_order'):
                form = OrderForm(request.POST)

                if form.is_valid():
                    # Get user profile
                    profile = Profile.objects.get(user=request.user)

                    # Save order
                    order = form.save(commit=False)
                    order.buyer = profile
                    order.save()

                    # Save items in order
                    for item in profile.cart_items.all():
                        OrderMembership(order=order, item=item).save()

                        # Delete items from cart
                        cart_item = CartMembership.objects.get(profile=profile, item=item)
                        cart_item.delete()

    else:
        form = OrderForm()

    user_profile = Profile.objects.get(user=request.user)
    sales = user_profile.cart_items.all()

    paginator = Paginator(sales, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'sales': sales,
        'cart_items': Profile.objects.get(user=request.user).cart_items.all(),
        'page_obj': page_obj,
        'form': form,
    }

    context['total_sum'] = round(sum(sale.price for sale in context['cart_items']),2)

    return render(request, 'accounts/cart.html', context)


@login_required
def shopping(request):
    user_profile = Profile.objects.get(user=request.user)
    orders = Order.objects.filter(buyer=user_profile)

    context = {
        'orders': orders,
    }
