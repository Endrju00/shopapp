from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Q

from .models import SaleOffer

# help functions
def check_filters(filters):
    # Categories
    if 'ALL' in filters["category"]:
        query = Q(category=SaleOffer.CATEGORY[0][0])
        for c in SaleOffer.CATEGORY[1:]:
            query |= Q(category=c[0])
    else:
        query = Q(category=filters["category"][0])

        if len(filters) > 1:
            for f in filters["category"][1:]:
                query |= Q(category=f)

    # Color
    if filters["color"][0]:
        query &= Q(item__color__contains=filters["color"][0])

    sales = SaleOffer.objects.filter(query)
    return sales

# Create your views here.
def index(request):
    if request.method == 'POST':
        filters = {}
        try:
            filters['category'] = request.POST.getlist('category')
            filters['color'] = request.POST.getlist('color')
            sales = check_filters(filters)
        except:
            sales = SaleOffer.objects.order_by('-pub_date')

    elif request.method == 'GET':
        sales = SaleOffer.objects.order_by('-pub_date')

    context = {
        'sales': sales,
        'categories': SaleOffer.CATEGORY,
    }

    return render(request, 'items/offers_list.html', context)


def detail(request, sale_id):
    sale = get_object_or_404(SaleOffer, pk=sale_id)
    return render(request, 'items/detail.html', {'sale': sale})


def filter(request, filter):
    filtered_sales = SaleOffer.objects.filter(category=filter)
    context = {
        'sales': filtered_sales,
        'categories': SaleOffer.CATEGORY,
    }

    return render(request, 'items/offers_list.html', context)
