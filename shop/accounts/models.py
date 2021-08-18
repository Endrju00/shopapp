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
        return f'{self.user.username} Profile'

class CartMembership(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    item = models.ForeignKey(SaleOffer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.profile.user}-{self.item.item.name}'
