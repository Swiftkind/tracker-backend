from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import SignupSerializer


class AccountAPI(ViewSet):
    """Account API
    """
    permission_classes = (AllowAny,)

    def register(self, request, *args, **kwargs):
        """ user register
        """
        serializer = SignupSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)