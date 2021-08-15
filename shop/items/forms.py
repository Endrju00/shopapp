from django.forms import ModelForm, Textarea
from .models import Item, SaleOffer


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class SaleOfferForm(ModelForm):
    class Meta:
        model = SaleOffer
        exclude = ['dealer']
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
