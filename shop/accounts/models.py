from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        default=5,
        validators = [MaxValueValidator(5), MinValueValidator(1)]
    )

    def __str__(self):
        return f'{self.user.username} Profile'
