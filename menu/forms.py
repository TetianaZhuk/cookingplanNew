import datetime

from django import forms

from meals.models import Meal
from menu.models import Day


class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        exclude = ('author', 'slug',)


class BreakfastForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ('breakfast',)


class LaunchForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ('launch',)


class DinnerForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ('dinner',)


class DateForm(forms.Form):
    start_date = datetime.date.today()
    end_date = datetime.date.today() + datetime.timedelta(weeks=1)
    start = forms.DateField(widget=forms.SelectDateWidget, label='Введите начальную дату', initial=start_date)
    end = forms.DateField(widget=forms.SelectDateWidget, label='Введите конечную дату', initial=end_date)
