from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormMixin, UpdateView, DeleteView

from ingredients.forms import IngredientForm
from menu.models import Day

from users.views import OnlyForAuthenticatedUsersView
from .forms import MealForm, MealIngredientsForm, AddMealToDayForm
from .models import Meal, MealIngredients, MealCategory


class AuthorMixin(UserPassesTestMixin):
    def test_func(self):
        slug = self.kwargs['slug']
        author = Meal.objects.get(slug=slug).author
        user = self.request.user
        return user == author


class MealsList(ListView):
    model = Meal
    context_object_name = 'meals'
    template_name = 'meals/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = MealCategory.objects.all()
        return context

    def get_queryset(self):
        q = self.request.GET.get('q')
        cat = self.request.GET.get('category')
        if q and cat:
            queryset = Meal.objects.filter(category__slug=cat, name__iregex=q)
        elif q:
            queryset = Meal.objects.filter(name__iregex=q)
        elif cat:
            queryset = Meal.objects.filter(category__slug=cat)
        else:
            queryset = Meal.objects.all()
        return queryset


class MealCreateView(LoginRequiredMixin, CreateView):
    model = Meal
    form_class = MealForm
    template_name = 'meals/create.html'
    login_url = 'users:login'

    def __init__(self):
        super().__init__()
        self.object = None

    def get_success_url(self):
        return reverse_lazy('meals:detail', kwargs={'slug': self.object.slug})

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # slug = slugify(form.cleaned_data['name'])
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            # self.object.slug = slug
            self.object.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class MealDetailView(FormMixin, DetailView):
    model = Meal
    form_class = MealIngredientsForm
    template_name = 'meals/detail.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('meals:detail', kwargs={'slug': self.get_object().slug})

    def get_context_data(self, **kwargs):
        kwargs['ingredients'] = MealIngredients.objects.filter(meal_id=self.get_object().id)
        return super().get_context_data(**kwargs)


class AddIngredientsToMeal(AuthorMixin, FormMixin, DetailView):
    model = Meal
    form_class = MealIngredientsForm
    template_name = 'meals/detail_old.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.ingredient = form.save(commit=False)
            self.ingredient.meal_id = Meal.objects.get(slug=kwargs['slug']).id
            self.ingredient.save()
            return redirect(reverse_lazy('meals:detail', kwargs={'slug': kwargs['slug']}))
        else:
            return self.form_invalid(form)


class MealUpdateView(AuthorMixin, LoginRequiredMixin, UpdateView):
    model = Meal
    form_class = MealForm
    template_name = 'meals/create.html'


class MealDeleteView(AuthorMixin, LoginRequiredMixin, DeleteView):
    model = Meal
    template_name = 'meals/delete.html'
    success_url = reverse_lazy('meals:list')


class MealIngredientsDeleteView(AuthorMixin, LoginRequiredMixin, DeleteView):
    model = MealIngredients

    def get_success_url(self, **kwargs):
        return reverse_lazy('meals:detail', kwargs={'slug': self.get_object().meal.slug})


class AddMealToDay(LoginRequiredMixin, UpdateView, FormMixin):
    model = Meal
    template_name = 'meals/add_to_day.html'

    def get_context_data(self, **kwargs):
        kwargs['form'] = AddMealToDayForm()
        return super().get_context_data(**kwargs)

    def post(self, *args, **kwargs):
        form = AddMealToDayForm(self.request.POST)
        if form.is_valid():
            kwargs['date'] = form.cleaned_data['date']
            kwargs['day_time'] = form.cleaned_data['day_time']
            meal = Meal.objects.get(slug=kwargs['slug'])
            try:
                day = Day.objects.get(slug=kwargs['date'])
            except Day.DoesNotExist:
                day = Day.objects.create(date=kwargs['date'], author=self.request.user)
            if kwargs['day_time'] == 'ЗАВТРАК':
                day.breakfast = meal
            elif kwargs['day_time'] == 'ОБЕД':
                day.launch = meal
            elif kwargs['day_time'] == 'УЖИН':
                day.dinner = meal
            day.save()
            return redirect(reverse('menu:list'))
        else:
            return self.form_invalid(form)
