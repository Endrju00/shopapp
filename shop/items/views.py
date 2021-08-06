from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from .models import SaleOffer

# Create your views here.
def index(request):
    if request.method == 'POST':
        sales = SaleOffer.objects.filter(category=request.POST['filter'])
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
