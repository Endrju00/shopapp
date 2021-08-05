from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from .models import SaleOffer

# Create your views here.
def index(request):
    latest_sales = SaleOffer.objects.order_by('-pub_date')
    context = {
        'latest_sales': latest_sales,
    }
    return render(request, 'items/index.html', context)


def detail(request, sale_id):
    sale = get_object_or_404(SaleOffer, pk=sale_id)
    return render(request, 'items/detail.html', {'sale': sale})
