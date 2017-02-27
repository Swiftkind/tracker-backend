from django.conf.urls import url

from rest_framework.authtoken import views

from .views import (
    LoginView,
    LogoutView,
    DashboardView,
    SignupView,
)

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^signup/$', SignupView.as_view(), name="signup"),

    url(r'^dashboard/$', DashboardView.as_view(), name="dashboard"),
]

account_urlpatterns = [
    # user token
    url(r'^token/$', views.obtain_auth_token, name="token"),
]