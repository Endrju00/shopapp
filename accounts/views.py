from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Profile, CartMembership, OrderMembership, Order, Notification
from .forms import CartForm, OrderForm, UserRegisterForm
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
        'profile': get_object_or_404(User, pk=user_id), # user obj (look at 'profile.html' to see the difference)
        'user': request.user,
        'sales': SaleOffer.objects.filter(item__dealer__id=user_id),
        'items': Item.objects.filter(dealer__id=user_id),
        'notifications': Notification.objects.filter(receiver=request.user.profile),
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
                cm_id = request.POST.get('delete_cart_item')
                cartmember = CartMembership.objects.get(id=cm_id)
                cartmember.delete()

            # Submit order
            if request.POST.get('submit_order'):
                form = OrderForm(request.POST)

                if form.is_valid():
                    # Get user profile
                    profile = Profile.objects.get(user=request.user)
                    cartmembers = CartMembership.objects.filter(profile=profile)

                    # check if there are items in the cart
                    if cartmembers:
                        # Save order
                        order = form.save(commit=False)
                        order.buyer = profile
                        order.save()
                        # Save items in order
                        for member in cartmembers:
                            if member.quantity > member.cart_item.item.quantity:
                                order.delete()
                                messages.warning(request,
                                 f'There are only {member.cart_item.item.quantity} piece(s) of {member.cart_item.title} available and you have ordered {member.quantity}.')
                                messages.warning(request, 'Please complete the order once again.')
                            else:
                                OrderMembership(order=order, order_item=member.cart_item, quantity=member.quantity).save()

                                # Notify the dealer
                                Notification(
                                    receiver=member.cart_item.item.dealer.profile,
                                    title=f'{order.buyer.user} bought your item.',
                                    sale_info=member.get_sale(),
                                    shipping_info=order.get_address(),
                                ).save()

                            # Delete items from cart
                            member.delete()
                    else:
                        redirect('cart')
                        messages.warning(request, 'You can not order nothing!')

    # Get data
    user_profile = Profile.objects.get(user=request.user)
    cartmembers = CartMembership.objects.filter(profile=user_profile)

    # Paginate sales in basket
    paginator = Paginator(cartmembers, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'total_sum': round(sum(cartmember.cart_item.price * cartmember.quantity for cartmember in cartmembers), 2),
        'num_of_items': sum(item.quantity for item in cartmembers),
        'page_obj': page_obj,
        'form': OrderForm(),
        'notifications': Notification.objects.filter(receiver=request.user.profile),
    }

    return render(request, 'accounts/cart.html', context)


@login_required
def order(request, order_id):
    # Get data
    order = get_object_or_404(Order, pk=order_id)

    if request.user.id != order.buyer.user.id:
        raise Http404

    ordermembers = OrderMembership.objects.filter(order=order)

    context = {
        'order': order,
        'ordermembers': ordermembers,
        'notifications': Notification.objects.filter(receiver=request.user.profile),
    }

    return render(request, 'accounts/order.html', context)


def notification(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)

    if request.user.id != notification.receiver.user.id:
        raise Http404

    context = {
        'notification': notification,
        'notifications': Notification.objects.filter(receiver=request.user.profile),
    }

    return render(request,'accounts/notification.html', context)
