from django.forms import ModelForm, Textarea, ModelChoiceField
from django.views.generic.edit import CreateView
from .models import Item, SaleOffer


class ItemForm(ModelForm):
    class Meta:
        model = Item
        exclude = ['dealer']


class SaleOfferForm(ModelForm):
    item = ModelChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.filter(dealer=user)

    class Meta:
        model = SaleOffer
        fields = '__all__'
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
