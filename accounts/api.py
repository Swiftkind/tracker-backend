from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404

from rest_framework.authentication import BasicAuthentication
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import (
            SignupSerializer, 
            LoginSerializer,
            AccountSerializer,
            ResetPasswordSerializer,
        )

from .models import Account

from .mixins import AccountMixin


class AccountAPI(AccountMixin, ViewSet):
    """Account API
    """
    permission_classes = (AllowAny,)

    def register(self, *args, **kwargs):
        """ user register
        """
        serializer = SignupSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def detail(self, *args, **kwargs):
        """ profile details
        """
        if self.request.user.is_authenticated():
            user = get_object_or_404(Account, email=self.request.user)
            serializer = AccountSerializer(user)
            return Response(serializer.data, status=200)
        return Response(status=204)

    def update(self, *args, **kwargs):
        """ profile update
        """
        user = get_object_or_404(Account, email=self.request.user)
        serializer = AccountSerializer(user, data=self.request.data)
        if serializer.is_valid():
            user = serializer.save()
            self.update_profile(user, self.request.data)
            self.update_profile_photo(user, self.request.FILES)

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def reset_password(self, *args, **kwargs):
        """ reset password
        """
        user = get_object_or_404(Account, email=self.request.user)
        serializer = ResetPasswordSerializer(data=self.request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({"old_password": "Wrong password."}, status=400)
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response('success', status=200)
        return Response(serializer.errors, status=400)


class LoginAPI(ViewSet):
    """ Login API
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)

    def login(self, *args, **kwargs):
        serializer = LoginSerializer(data=self.request.data)
        if serializer.is_valid():
            login(self.request, serializer.user_cache)

            return Response(serializer.data, status=204)
        return Response(serializer.errors, status=400)

    def logout(self, *args, **kwargs):
        logout(self.request)
        return Response(status=204)