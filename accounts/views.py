from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Profile, CartMembership, OrderMembership, Order
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

            if request.POST.get("delete_item"):
                item_id = request.POST.get("delete_item")
                item = Item.objects.get(id=item_id)
                messages.success(request, f'Item {item} and all of the sales with it have been deleted.')
                item.delete()

            elif request.POST.get("delete_sale"):
                sale_id = request.POST.get("delete_sale")
                sale = SaleOffer.objects.get(id=sale_id)
                messages.success(request, f'Sale offer: {sale.title} has been deleted.')
                sale.delete()

    context = {
        'profile': User.objects.get(id=user_id),
        'user': request.user,
        'sales': SaleOffer.objects.filter(item__dealer__id=user_id),
        'items': Item.objects.filter(dealer__id=user_id),
    }

    if request.user.is_authenticated:
        context['orders'] = Order.objects.filter(buyer=context['profile'].profile)
        context['cart_items'] = Profile.objects.get(user=request.user).cart_items.all()

    return render(request, 'accounts/profile.html', context)


@login_required
def cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            # Delete item from the cart
            if request.POST.get('delete_cart_item'):
                sale_id = request.POST.get('delete_cart_item')
                form = OrderForm()
                profile = Profile.objects.get(user=request.user)
                sale = SaleOffer.objects.get(id=sale_id)
                cartmember = CartMembership.objects.get(profile=profile, cart_item=sale)
                cartmember.delete()

            # Submit order
            if request.POST.get('submit_order'):
                form = OrderForm(request.POST)

                if form.is_valid():
                    # Get user profile
                    profile = Profile.objects.get(user=request.user)

                    # check if there are items in the cart
                    if profile.cart_items.all():
                        # Save order
                        order = form.save(commit=False)
                        order.buyer = profile
                        order.save()
                        # Save items in order
                        for item in profile.cart_items.all():
                            OrderMembership(order=order, order_item=item).save()
                            # Delete items from cart
                            cartmember = CartMembership.objects.get(profile=profile, cart_item=item)
                            cartmember.delete()
                    else:
                        redirect('cart')
                        messages.warning(request, 'You can not order nothing!')

    else:
        form = OrderForm()

    # Get data
    user_profile = Profile.objects.get(user=request.user)
    sales = user_profile.cart_items.all()

    # Paginate sales in basket
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


def order(request, order_id):
    # Get data
    order = Order.objects.get(id=order_id)
    items = order.order_items.all()

    context = {
        'order': order,
        'items': items,
    }

    return render(request, 'accounts/order.html', context)
