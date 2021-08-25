from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, OrderMembership


# if user is created then create a profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# if OrderMembership is created reduce the quantity of item in the offer
@receiver(post_save, sender=OrderMembership)
def reduce_quantity(sender, instance, created, **kwargs):
    if created:
        item = instance.order_item.item
        if item.quantity >= instance.quantity:
            item.quantity -= instance.quantity
            item.save()
