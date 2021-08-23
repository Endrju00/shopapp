from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from items.models import SaleOffer

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        default=5,
        validators = [MaxValueValidator(5), MinValueValidator(1)]
    )

    cart_items = models.ManyToManyField(
        SaleOffer,
        through='CartMembership',
    )

    def __str__(self):
        return f'{self.user.username} profile'

    class Meta:
        ordering = ['-id']


class CartMembership(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    item = models.ForeignKey(SaleOffer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.profile.user}-{self.item.item.name}'

    class Meta:
        ordering = ['-id']


class Order(models.Model):
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    items = models.ManyToManyField(
        SaleOffer,
        through='OrderMembership',
    )

    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=6)

    IN_PROGRESS = 'In progress'
    SENT = 'Sent'
    DELIVERED = 'Delivered'

    STATUS = [
        (IN_PROGRESS, 'In progress'),
        (SENT, 'Sent'),
        (DELIVERED, 'Delivered'),
    ]

    status = models.CharField(max_length=20, choices=STATUS, default=IN_PROGRESS)

    def __str__(self):
        return f'Order #{self.id}'

    class Meta:
        ordering = ['-id']


class OrderMembership(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(SaleOffer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.item} in #{self.order.id}'

    class Meta:
        ordering = ['-id']
