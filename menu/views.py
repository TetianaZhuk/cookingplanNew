import urllib.parse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import render, redirect
import datetime

from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import FormMixin, UpdateView, DeleteView

from ingredients.models import Ingredient
from meals.forms import MealIngredientsForm
from meals.models import Meal
from menu.forms import DayForm, DateForm, BreakfastForm, LaunchForm, DinnerForm
from menu.models import Day


def index(request):
    template_name = 'index.html'
    context = {'title': 'Главная'}
    return render(request, template_name, context)


class DayListView(ListView):
    model = Day
    template_name = 'menu/list.html'
    context_object_name = 'days'


class DayCreateView(CreateView, FormMixin):
    model = Day
    fields = '__all__'
    template_name = 'menu/create.html'
    context_object_name = 'days'
    success_url = 'menu:list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DateForm()
        return context

    def post(self, request, *args, **kwargs):
        form = DateForm(self.request.POST)
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid()

    def form_valid(self, form, **kwargs):
        start = form.cleaned_data['start']
        end = form.cleaned_data['end']
        while start <= end:
            try:
                day = Day.objects.get(date=start, author=self.request.user)
            except Day.DoesNotExist:
                day = Day.objects.create(date=start, author=self.request.user)
            start += datetime.timedelta(days=1)
        return redirect("menu:list")


class LaunchCreateView(LoginRequiredMixin, CreateView):
    model = Day
    template_name = 'menu/create_launch.html'
    form_class = LaunchForm
    success_url = reverse_lazy('menu:list')


class DinnerCreateView(CreateView):
    model = Day
    template_name = 'menu/create_dinner.html'
    form_class = DinnerForm
    success_url = reverse_lazy('menu:list')


class BreakfastCreateView(CreateView):
    model = Day
    template_name = 'menu/create_day.html'
    form_class = BreakfastForm
    success_url = reverse_lazy('menu:list')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, **kwargs):
        day = Day.objects.get(slug=kwargs['slug'])
        day.breakfast = form.cleaned_data['breakfast']
        day.save()
        return redirect("menu:list")


class LaunchCreateView(CreateView):
    model = Day
    template_name = 'menu/create_day.html'
    form_class = LaunchForm
    success_url = reverse_lazy('menu:list')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, **kwargs):
        day = Day.objects.get(slug=kwargs['slug'])
        day.launch = form.cleaned_data['launch']
        day.save()
        return redirect("menu:list")


class DinnerCreateView(CreateView):
    model = Day
    template_name = 'menu/create_day.html'
    form_class = DinnerForm
    success_url = reverse_lazy('menu:list')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, **kwargs):
        day = Day.objects.get(slug=kwargs['slug'])
        day.dinner = form.cleaned_data['dinner']
        day.save()
        return redirect("menu:list")


#
# class MenuListView(ListView, FormMixin):
#     model = Day
#     template_name = 'menu/list.html'
#     context_object_name = 'days'
#     form_class = DateForm
#
#     def get(self, request, *args, **kwargs):
#         start = (datetime.date.today()).strftime("%Y-%m-%d")
#         end = (datetime.date.today() + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d")
#         kwargs['start'] = start
#         kwargs['end'] = end
#         self.object_list = self.get_queryset(**kwargs)
#         return super().render_to_response(self.get_context_data(**kwargs))
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(self.request.POST)
#         if form.is_valid():
#             kwargs['start'] = (form.cleaned_data['start']).strftime("%Y-%m-%d")
#             kwargs['end'] = (form.cleaned_data['end']).strftime("%Y-%m-%d")
#             self.object_list = self.get_queryset(**kwargs)
#         else:
#             return self.form_invalid()
#         return super().render_to_response(self.get_context_data(**kwargs))
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['date_form'] = DateForm(initial={'start': kwargs['start'], 'end': kwargs['end']})
#         return context
#
#     def get_queryset(self, **kwargs):
#         if self.request.method == "GET":
#             self.queryset = Day.objects.none()
#         if self.request.method == "POST":
#             start = datetime.datetime.strptime(kwargs['start'], "%Y-%m-%d")
#             end = datetime.datetime.strptime(kwargs['end'], "%Y-%m-%d")
#             start_tmp = start
#             while start_tmp <= end:
#                 try:
#                     day = Day.objects.get(date=start_tmp, author=self.request.user)
#                 except Day.DoesNotExist:
#                     day = Day(date=start_tmp, author=self.request.user)
#                     day.save()
#                 start_tmp += datetime.timedelta(days=1)
#             self.queryset = Day.objects.filter(date__range=(start, end))
#         return self.queryset
#         # while start <= end:
#         #     try:
#         #         Day.objects.get(date=start.strftime("%Y-%m-%d"))
#         #     except Day.DoesNotExist:
#         #         Day.objects.create(date=start, author=self.request.user)
#         #         start += datetime.timedelta(days=1)
#         #         return Day.objects.filter(date__range=(start, end))
#
#     # TODO добавить фильтрацию по автору


class DayDeleteView(DeleteView):
    model = Day
    template_name = 'menu/list.html'
    success_url = reverse_lazy('menu:list')


#


#


def build_url(*args, **kwargs):
    get = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)
    if get:
        url += '?' + urllib.parse.urlencode(get)
    return url


def menuList(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    template_name = 'menu/list.html'
    days = Day.objects.filter(date__range=(start, end))
    context = {'title': 'Меню',
               'days': days}
    return render(request, template_name, context)


class ShoppingListView(ListView):
    model = Ingredient
    template_name = 'menu/list.html'
    context_object_name = 'shopping_list'

    def post(self):
        pass



def menuSearch(request):
    template_name = 'menu/create.html'
    start = datetime.date.today()
    end = datetime.date.today() + datetime.timedelta(weeks=1)
    form = DatesChoiceForm(initial={'start': start, 'end': end})
    context = {'title': 'Добавить меню',
               'form': form,
               'button': 'Искать'}
    if request.method == 'POST':
        form = DatesChoiceForm(request.POST)
        if form.is_valid():
            start = (form.cleaned_data['start'])
            end = (form.cleaned_data['end'])
            url = build_url('menu:list', get={'start': start, 'end': end})
            return redirect(url)
    return render(request, template_name, context)


def create(request):
    template_name = 'menu/create.html'
    start = datetime.date.today()
    end = datetime.date.today() + datetime.timedelta(weeks=1)
    form = DatesChoiceForm(initial={'start': start, 'end': end})
    context = {'title': 'Добавить меню',
               'form': form,
               'button': 'Сохранить'}
    if request.method == 'POST':
        form = DatesChoiceForm(request.POST)
        if form.is_valid():
            start = (form.cleaned_data['start'])
            end = (form.cleaned_data['end'])
            start_tmp = start
            while start_tmp <= end:
                Day.objects.create(date=start_tmp, author=request.user)
                start_tmp += datetime.timedelta(days=1)
            print(start, type(start), end, type(end))
            url = build_url('menu:list', get={'start': start, 'end': end})
            return redirect(url)

    return render(request, template_name, context)

# class WeekCreateView(CreateView):
#     model = Week
#     form_class = DayChoiceForm
#     template_name = 'menu/create.html'
#     extra_context = {'title': 'Создать меню недели'}


# class DayCreateView(CreateView):
#     model = Day
#     form_class = DayForm
#     template_name = 'menu/create_day.html'
#     extra_context = {'title': 'Создать меню дня'}
