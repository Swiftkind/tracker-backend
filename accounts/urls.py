from django.conf.urls import url
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
