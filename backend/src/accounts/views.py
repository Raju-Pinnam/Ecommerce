from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.views.generic.base import View
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestUser


def guest_register(request):
    form = GuestForm(request.POST or None)
    context = {
        'form': form,
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_post or next_ or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email = GuestUser.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect('accounts:register')


class LoginUser(TemplateView):
    template_name = 'accounts/login_page.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        request = self.request

        _form = self.form_class(request.POST or None)
        context = super(LoginUser, self).get_context_data(**kwargs)
        context['form'] = _form
        return context

    def post(self, *args, **kwargs):
        request = self.request
        _form = self.form_class(request.POST or None)
        print(request.POST)
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if _form.is_valid():
            username = _form.cleaned_data.get('username')
            password = _form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    del request.session['guest_email_id']
                except:
                    pass
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
                return redirect('basic:home')
            else:
                return render(request, self.template_name, {'form': _form})
        return render(request, self.template_name, {'form': _form})


class Logout(View):
    def get(self, *args, **kwargs):
        request = self.request
        logout(request)
        return redirect('accounts:login')


class RegisterUser(TemplateView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    User = get_user_model()

    def get_context_data(self, **kwargs):
        request = self.request
        _from = self.form_class(request.POST or None)
        context = super(RegisterUser, self).get_context_data(**kwargs)
        context['form'] = _from
        return context

    def post(self, *args, **kwargs):
        request = self.request
        _form = self.form_class(request.POST or None)
        if _form.is_valid():
            username = _form.cleaned_data.get('name')
            email = _form.cleaned_data.get('email')
            password = _form.cleaned_data.get('password')
            new_user = self.User.objects.create_user(name=username, email=email, password=password)
            print('new user', new_user)
            return redirect('accounts:login')

        return render(request, self.template_name, {'form': _form})
