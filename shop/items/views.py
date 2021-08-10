from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Item, SaleOffer

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

# Create your views here.
def index(request):
    if request.method == 'POST':
        filters = {}
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

    elif request.method == 'GET':
        sales = SaleOffer.objects.order_by('-pub_date')

    paginator = Paginator(sales, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'sales': sales,
        'categories': SaleOffer.CATEGORY,
        'conditions': Item.CONDITION,
        'page_obj': page_obj,
    }

    return render(request, 'items/offers_list.html', context)


def detail(request, sale_id):
    sale = get_object_or_404(SaleOffer, pk=sale_id)
    return render(request, 'items/detail.html', {'sale': sale})


def filter(request, filter):
    filtered_sales = SaleOffer.objects.filter(category=filter)
    print(filtered_sales)

    paginator = Paginator(filtered_sales, 6)
    print(paginator)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'sales': filtered_sales,
        'categories': SaleOffer.CATEGORY,
        'conditions': Item.CONDITION,
        'page_obj': page_obj,
    }

    return render(request, 'items/offers_list.html', context)
