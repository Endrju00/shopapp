from django.db import models
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=50)
    producer = models.CharField(max_length=50)
    weight = models.PositiveIntegerField(help_text='Please pass the weight in grams.')
    height = models.PositiveIntegerField(help_text='Please pass the height in centimeters.')
    length = models.PositiveIntegerField(help_text='Please pass the length in centimeters.')
    width = models.PositiveIntegerField(help_text='Please pass the width in centimeters.')

    def __str__(self):
        return f"{self.name} {self.producer}"


class SaleOffer(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.CharField(max_length=300)
    pub_date = models.DateTimeField(default=timezone.now, editable=False)
    exp_date = models.DateTimeField(default=timezone.now() + timedelta(days=30), editable=False)

    HOUSE_AND_GARDEN = 'HG'
    ELECTRONICS = 'EL'
    FASHION = 'FA'
    AUTOMOTIVE = 'AM'
    SPORT = 'SP'
    BEAUTY = 'BE'
    HEALTH = 'HE'
    OTHER = 'OT'
    CATEGORY = [
        (HOUSE_AND_GARDEN, 'House and Garden'),
        (ELECTRONICS, 'Electronics'),
        (FASHION, 'Fashion'),
        (AUTOMOTIVE, 'Automotive'),
        (SPORT, 'Sport'),
        (BEAUTY, 'Beauty'),
        (HEALTH, 'Health'),
        (OTHER, 'Other'),
    ]

    category = models.CharField(max_length=2, choices=CATEGORY, default=OTHER)

    def __str__(self):
        return f"{self.item.name} for {self.price} PLN"
