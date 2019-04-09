from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

from . import serializers
from . import models


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class UserPreferences(generics.RetrieveUpdateAPIView):
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

class ListDogs(generics.RetrieveUpdateAPIView):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        queryset = self.get_queryset()

        if self.kwargs.get('pk') == -1:
            dog = queryset.get(pk=1)
        else:
            dog = self.get_queryset().first()

        return dog


#kwargs.get is de pk die binnenkomt
#get_object gets a single item