from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import LoginForm, RegistrationForm
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import  PermissionRequiredMixin


class OnlyForAuthenticatedUsersView(PermissionRequiredMixin, TemplateView):
    permission_required = 'meals.delete_meal', 'meals.add_meal', 'meals.change_meal'
    template_name = 'users/secured.html'
    login_url = reverse_lazy('users:login')
    extra_context = {'title': 'Only for authenticated users'}


def login_view(request):
    form = LoginForm()
    if request.method == 'GET':
        return render(request, 'users/login.html', {'form': form})
    elif request.method == 'POST':
        try:
            user = authenticate(username=request.POST.get('login'),
                                password=request.POST.get('password'))
            if user:
                login(request, user)
        except Exception as e:
            print(e)
            return render(request, 'users/login.html', {'form': LoginForm(data=request.POST)})
        next = request.GET.get('next', '/')
        return redirect(next)


def logout_view(request):
    logout(request)
    return redirect("/")


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            # registered_user.send(sender=User, user=new_user)
            return render(request, 'users/secured.html', {'user': new_user})

    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})