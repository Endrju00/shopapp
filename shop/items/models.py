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
    color = models.CharField(max_length=50, default="Unknown")

    NEW = 'N'
    USED = 'U'
    NOT_SPECIFIED = 'NS'
    CONDITION = [
        (NEW, 'New'),
        (USED, 'Used'),
        (NOT_SPECIFIED, 'Not Specified'),
    ]
    condition = models.CharField(max_length=2, choices=CONDITION, default=NOT_SPECIFIED)

    def __str__(self):
        return f"{self.name} {self.producer}"

    def get_condition(self):
        for c in self.CONDITION:
            if c[0] == self.condition:
                return c[1]
        return 'Not Specified'


class SaleOffer(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, default=item.name)
    first_image = models.ImageField(default='default.jpg', upload_to='items', help_text="This image will be shown in search results.")
    second_image = models.ImageField(default='default.jpg', upload_to='items', help_text="Secondary image.")
    price = models.FloatField()
    description = models.CharField(max_length=300)
    quantity = models.PositiveIntegerField(default=1, help_text='Please pass the number of pieces in the package.')
    free_delivery = models.BooleanField(default=False)
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
