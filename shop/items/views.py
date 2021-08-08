from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Q

from .models import SaleOffer

# help functions
def check_filters(filters):
    if 'ALL' in filters:
        sales = SaleOffer.objects.order_by('-pub_date')
    else:
        query = Q(category=filters[0])

        if len(filters) > 1:
            for f in filters[1:]:
                query |= Q(category=f)

        sales = SaleOffer.objects.filter(query)
    return sales

# Create your views here.
def index(request):
    if request.method == 'POST':
        try:
            filters = request.POST.getlist('filter')
            sales = check_filters(filters)
        except:
            sales = SaleOffer.objects.order_by('-pub_date')
    else:
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
