import datetime

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from meals.models import Meal
from django.utils import timezone


class Day(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    date = models.DateField()
    slug = models.SlugField(max_length=10, unique=True, verbose_name='URL')

    breakfast = models.ForeignKey(Meal,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  related_name='breakfast')
    launch = models.ForeignKey(Meal,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name='launch')
    dinner = models.ForeignKey(Meal,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name='dinner')

    class Meta:
        unique_together = ('author', 'date')
        ordering = ['-date']

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.date.strftime("%Y-%m-%d"))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('menu:detail', kwargs={'slug': self.slug})
