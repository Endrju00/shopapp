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
    cart_item = models.ForeignKey(SaleOffer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.profile.user}-{self.cart_item.item.name}'

    class Meta:
        ordering = ['-id']

    def get_sale(self):
        return f'{self.cart_item.item} in {self.cart_item} offer.' + '\n' + f'Quantity: {self.quantity}'


class Order(models.Model):
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    order_items = models.ManyToManyField(
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

    def get_address(self):
        return f'Country: {self.country}' + '\n' + f'City: {self.city}' + '\n' + f'Street: {self.street}' + '\n' + f'Postal code: {self.postal_code}' + '\n'


class OrderMembership(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_item = models.ForeignKey(SaleOffer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.order_item} in #{self.order.id}'

    class Meta:
        ordering = ['-id']


class Notification(models.Model):
    sender_id = models.PositiveIntegerField()
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(default='Title', max_length=50)
    sale_info = models.TextField(max_length=255, blank=True)
    shipping_info = models.TextField(max_length=255, blank=True)

    ORDER = 'order'
    SHIPPING = 'shipping'

    TYPE = [
        (ORDER, 'Order'),
        (SHIPPING, 'Shipping'),
    ]

    type = models.CharField(max_length=20, choices=TYPE, default=ORDER)

    def __str__(self):
        return f'Notification #{self.id}'

    class Meta:
        ordering = ['-id']
