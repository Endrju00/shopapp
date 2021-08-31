from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Item(models.Model):
    dealer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    producer = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(help_text='Please pass the quantity of this item that you have to sell.', default=1)

    weight = models.FloatField(help_text='Please pass the weight in kilograms.', validators=[MinValueValidator(0)])
    height = models.FloatField(help_text='Please pass the height in meters.', validators=[MinValueValidator(0)])
    length = models.FloatField(help_text='Please pass the length in meters.', validators=[MinValueValidator(0)])
    width = models.FloatField(help_text='Please pass the width in meters.', validators=[MinValueValidator(0)])
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

    class Meta:
        ordering = ['-id']


class SaleOffer(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, default=item.name)

    # during real deployment
    first_image = models.ImageField(default='default.jpg', upload_to='items', help_text="This image will be shown in search results.")
    second_image = models.ImageField(default='default.jpg', upload_to='items', help_text="Secondary image.")

    # for project purposes
    first_image_url = models.CharField(max_length=255, blank=True, null=True)
    second_image_url = models.CharField(max_length=255, blank=True, null=True)

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


    class Meta:
        ordering = ['-pub_date']
