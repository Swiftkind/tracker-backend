from django.contrib.auth import login, logout

from rest_framework.authentication import BasicAuthentication
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import (
            SignupSerializer, 
            LoginSerializer,
            AccountSerializer,
        )

from .models import Account


class AccountAPI(ViewSet):
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


class AccountProfileAPI(ViewSet):
    """ User profile 
    """
    def detail(self, *args, **kwargs):
        """ profile details
        """
        serializer = AccountSerializer(self.request.user)
        return Response(serializer.data, status=200)
