from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token

from .views import (
    LoginView,
    LogoutView,
    DashboardView,
    SignupView,
)

from .api import AccountAPI, LoginAPI, ProfilePhotoAPI

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^signup/$', SignupView.as_view(), name="signup"),

    url(r'^dashboard/$', DashboardView.as_view(), name="dashboard"),
]

account_url = AccountAPI.as_view({'post': 'register',
                                  'get': 'detail',
                                  'put': 'update',
                                })
login_url = LoginAPI.as_view({'post': 'login'})
logout_url = LoginAPI.as_view({'get': 'logout'})

profile_photo = ProfilePhotoAPI.as_view({'put': 'photo'})

account_urlpatterns = [
    # jwt token
    url(r'^token/', obtain_jwt_token),

    url(r'^account/$', account_url, name='account'),
    url(r'^login/$', login_url, name="user_login"),
    url(r'^logout/$', logout_url, name="user_logout"),
    url(r'^photo/$', profile_photo, name="profile_photo"),
    url(r'^accounts/', AccountAPI.as_view({
        'get': 'list',
    }), name="accounts")
]
