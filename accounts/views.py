from django.conf import settings
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from projects.models import Project
from .forms import LoginForm, SignupForm


class LoginView(TemplateView):
    """ login view
    """
    template_name = 'accounts/login.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {
            'form': LoginForm(),
        })

    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST)
        
        if form.is_valid():
            # user credentials are valid,
            # add user to the session
            login(self.request, form.user_cache)
            return HttpResponseRedirect(reverse('dashboard'))

        return render(self.request, self.template_name, {
            'form': form,
        })


class LogoutView(LoginRequiredMixin, View):
    """ logout view
    """
    def get(self, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse('login'))


class SignupView(TemplateView):
    """ registration view
    """
    template_name = 'accounts/signup.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {
            'form': SignupForm(),
        })

    def post(self, *args, **kwargs):
        form = SignupForm(self.request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('dashboard'))

        return render(self.request, self.template_name, {
            'form': form,
        })


class DashboardView(LoginRequiredMixin, TemplateView):
    """ dashboard view
    """
    template_name = 'accounts/dashboard.html'
    def get(self, *args, **kwargs):
        #Superuser/staff can show all the list projects and weekly hours.
        if self.request.user.is_superuser or self.request.user.is_staff:
            projects = Project.objects.all()
        else:
        #Only the request user can show his list of projects and weekly hours.
            projects = Project.objects.filter(account=self.request.user)
        return render(self.request, self.template_name, {
            'projects': projects,
        })


class BaseView(TemplateView):
    """ base view
    """
    template_name = 'base.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {})

