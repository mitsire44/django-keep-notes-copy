from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class note(models.Model):
    colours = [
        ('Azure', 'Default'),
        ('Yellow', 'Yellow'),
        ('Orange', 'Orange'),
        ('Salmon', 'Salmon'),
        ('Aqua', 'Cyan'),
        ('Chartreuse', 'Lime Green'),
        ('Gray', 'Gray'),
    ]
    title = models.CharField(max_length=20,blank=True)
    colour = models.CharField(
        max_length=20,
        choices=colours,
        default='White',
    )
    desc = models.TextField()
    date = models.DateField(auto_now=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title
