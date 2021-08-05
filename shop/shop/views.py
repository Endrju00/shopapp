from django.views.generic import TemplateView

from items.models import SaleOffer

# Create your views here.
class HomePage(TemplateView):
    template_name = 'index.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [x[1] for x in SaleOffer.CATEGORY]
        return context
