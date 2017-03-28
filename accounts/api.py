from django.contrib.auth import login, logout

from rest_framework.authentication import BasicAuthentication
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from rest_framework.views import APIView

from .serializers import (
                    SignupSerializer, 
                    LoginSerializer,
                    AccountSerializer, 
                    ProfilePhotoSerializer
                )

from .models import Account

class AccountAPI(ViewSet):
    """Account API
    """
    permission_classes = (AllowAny,)

    def detail(self, *args, **kwargs):
        """logged in user data
        """
        if self.request.user.is_authenticated():
            serializer = AccountSerializer(self.request.user, context={'request': self.request})
            return Response(serializer.data, status=200)
        return Response(status=204)

    def register(self, *args, **kwargs):
        """ user register
        """
        serializer = SignupSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, *args, **kwargs):
        """ user update
        """
        if self.request.user.is_authenticated():
            serializer = AccountSerializer(self.request.user, data=self.request.data, context={'request': self.request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response(status=401)

    def list(self, *args, **kwargs):
        """all accounts data
        """
        accounts = Account.objects.filter(is_admin=False)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=200)

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


class ProfilePhotoAPI(ViewSet):
    """ uplaod profile photo
    """
    parser_classes = (FormParser, MultiPartParser)

    def photo(self, *args, **kwargs):
        serializer = ProfilePhotoSerializer(self.request.user, data=self.request.data, context={'request': self.request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
