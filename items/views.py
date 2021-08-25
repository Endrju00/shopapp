from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import Item, SaleOffer
from .forms import SaleOfferForm, ItemForm
from accounts.models import Profile, CartMembership
from accounts.forms import CartForm

# help functions
def check_filters(filters):
    # Search bar functionality
    if filters['search-bar']:
        words = filters['search-bar'][0].split()
        query = Q(title__contains=words[0])

        for word in words[1:]:
            query |= Q(title__contains=word)

        sales = SaleOffer.objects.filter(query)
        return sales

    # Categories
    if 'ALL' in filters["category"] or not filters["category"]:
        query = Q(category=SaleOffer.CATEGORY[0][0])
        for c in SaleOffer.CATEGORY[1:]:
            query |= Q(category=c[0])
    else:
        query = Q(category=filters["category"][0])

        if len(filters) > 1:
            for f in filters["category"][1:]:
                query |= Q(category=f)

    # Condition
    if filters["condition"]:
        query &= Q(item__condition=filters["condition"][0])

    # Delivery
    if filters["delivery"]:
        query &= Q(free_delivery=True)

    # Color
    if filters["color"][0]:
        query &= Q(item__color__contains=filters["color"][0])

    # Producer
    if filters["producer"][0]:
        query &= Q(item__producer__contains=filters["producer"][0])


    sales = SaleOffer.objects.filter(query)
    return sales


def in_cart(sale, profile):
    return CartMembership.objects.filter(profile=profile, cart_item=sale)

# Create your views here.
def index(request):
    if request.method == 'POST':
        if request.POST.get('submit_filters'):
            filters = {}
            # Get the filters
            try:
                filters['search-bar'] = request.POST.getlist('search-bar')
                filters['category'] = request.POST.getlist('category')
                filters['condition'] = request.POST.getlist('condition')
                filters['delivery'] = request.POST.getlist('free_delivery')
                filters['color'] = request.POST.getlist('color')
                filters['producer'] = request.POST.getlist('producer')
                sales = check_filters(filters)
            except:
                sales = SaleOffer.objects.order_by('-pub_date')

        # Clicked the buy now button
        elif request.POST.get('buy'):
            sale_id = request.POST.get('buy')
            if request.user.is_authenticated:
                sale = SaleOffer.objects.get(id=sale_id)
                profile = Profile.objects.get(user=request.user)
                cartmember = CartMembership(profile=profile, cart_item=sale, quantity=1)

                if not in_cart(sale, profile):
                    messages.success(request, 'An item has been added to the cart.')
                    cartmember.save()
                else:
                    cartmember = CartMembership.objects.get(profile=profile, cart_item=sale)
                    cartmember.quantity += 1
                    cartmember.save()
                    messages.success(request, f'Another {sale.title} has been added.')


                return redirect('cart')

            else:
                messages.warning(request, 'You must be logged in to buy an item.')
                return redirect('login')

    elif request.method == 'GET':
        sales = SaleOffer.objects.order_by('-pub_date')

    # Paginate sales
    paginator = Paginator(sales, 60)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'sales': sales,
        'categories': SaleOffer.CATEGORY,
        'conditions': Item.CONDITION,
        'page_obj': page_obj,
    }

    if request.user.is_authenticated:
        context['cart_items'] = Profile.objects.get(user=request.user).cart_items.all()

    return render(request, 'items/offers_list.html', context)


def detail(request, sale_id):
    # Get data
    sale = get_object_or_404(SaleOffer, pk=sale_id)
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CartForm(request.POST)
            if form.is_valid():
                # Edit CartMembershipForm data
                cartmember = form.save(commit=False)
                cartmember.profile = profile
                cartmember.cart_item = sale

                if not in_cart(sale, profile):
                    messages.success(request, 'An item has been added to the cart.')
                    cartmember.save()
                else:
                    cartmember = CartMembership.objects.get(profile=profile, cart_item=sale)
                    cartmember.quantity += 1
                    cartmember.save()
                    messages.success(request, f'Another {sale.title} has been added.')

                if request.POST.get("buy"):
                    return redirect('cart')

                elif request.POST.get('add'):
                    return HttpResponseRedirect(reverse('items:detail', args=[sale.id]))
        else:
            messages.warning(request, 'You must be logged in to buy an item.')
            return redirect('login')
    else:
        form = CartForm()

    context = {
        'sale': sale,
        'form': form,
    }

    if request.user.is_authenticated:
        context['cart_items'] = Profile.objects.get(user=request.user).cart_items.all()

    return render(request, 'items/detail.html', context)


def filter(request, filter):
    # Get sales that belong to special category
    filtered_sales = SaleOffer.objects.filter(category=filter)

    # Paginate sales
    paginator = Paginator(filtered_sales, 60)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'sales': filtered_sales,
        'categories': SaleOffer.CATEGORY,
        'conditions': Item.CONDITION,
        'page_obj': page_obj,
    }

    if request.user.is_authenticated:
        context['cart_items'] = Profile.objects.get(user=request.user).cart_items.all()

    return render(request, 'items/offers_list.html', context)

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            # Set the current user as dealer
            item = form.save(commit=False)
            item.dealer = request.user
            item.save()
            return redirect('items:add_sale')
    else:
        form = ItemForm()

    context = {
        'form': form,
        'cart_items': Profile.objects.get(user=request.user).cart_items.all()
    }

    return render(request, 'items/add_item.html', context)


@login_required
def create_sale(request):
    if request.method == 'POST':
        form = SaleOfferForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('items:index')
    else:
        form = SaleOfferForm(request.user)

    context = {
        'form': form,
        'cart_items': Profile.objects.get(user=request.user).cart_items.all()
    }

    return render(request, 'items/create.html', context)
