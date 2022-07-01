from django.db import models

# Create your models here.
from django.urls import reverse


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    UN_CHOICES = (
        ('кг', 'килограмм'),
        ('л', 'литр'),
        ('г', 'грамм'),
        ('мл', 'миллилитр'),
        ('шт', 'штука')
    )
    units = models.CharField(max_length=20, choices=UN_CHOICES, blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('ingredients:detail', kwargs={'pk': self.pk})