from django.conf.urls import url

from rest_framework.authtoken import views

from .views import (
    LoginView,
    LogoutView,
    DashboardView,
    SignupView,
)

from .api import AccountAPI, LoginAPI

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^signup/$', SignupView.as_view(), name="signup"),

    url(r'^dashboard/$', DashboardView.as_view(), name="dashboard"),
]

signup_url = AccountAPI.as_view({'post': 'register'})
account_detail_url = AccountAPI.as_view({'get': 'detail'})
account_update_url = AccountAPI.as_view({'put': 'update'})
reset_password_url = AccountAPI.as_view({'put': 'reset_password'})

login_url = LoginAPI.as_view({'post': 'login'})
logout_url = LoginAPI.as_view({'post': 'logout'})

account_urlpatterns = [
    # user token
    url(r'^token/$', views.obtain_auth_token, name="token"),

    url(r'^signup/$', signup_url, name='register'),
    url(r'^login/$', login_url, name="user_login"),
    url(r'^logout/$', logout_url, name="user_logout"),

    url(r'^user/detail/$', account_detail_url, name='user_details'),
    url(r'^user/update/$', account_update_url, name='user_update'),
    url(r'^user/reset_password/$', reset_password_url, name='reset_password')

]