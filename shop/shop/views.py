from django.views.generic import TemplateView
from random import choice
from django import template


from items.models import SaleOffer


# Help functions
def get_random_sales(sales):
    if len(sales) >= 3:
        random_sales = [choice(sales)]
        while len(random_sales) < 3:
            sale = choice(sales)
            if sale not in random_sales:
                random_sales.append(sale)
    else:
        return None

    return random_sales

def get_suggestions(sales, categories, suggestions):
    for category in categories.keys():
        suggestions[category] = get_random_sales(sales.filter(category=category))


# Create your views here.
class HomePage(TemplateView):
    template_name = 'index.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = dict(SaleOffer.CATEGORY)
        context['suggestions'] = {}
        get_suggestions(SaleOffer.objects.all(), context['categories'], context['suggestions'])
        return context
