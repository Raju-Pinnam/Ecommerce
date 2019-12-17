from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from .forms import ContactForm


class HomePage(TemplateView):
    template_name = 'normal/home_page.html'

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['first_try'] = 'Hello world'
        return context


class ContactPage(TemplateView):
    template_name = 'normal/contact_page.html'
    _form = ContactForm

    def get_context_data(self, **kwargs):
        c_from = self._form()
        context = super(ContactPage, self).get_context_data(**kwargs)
        context['form'] = c_from
        return context

    def post(self, *args, **kwargs):
        c_from = self._form(self.request.POST or None)
        if c_from.is_valid():
            return redirect('basic:contact')
        return render(self.request, self.template_name, {'form': c_from})
