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

    lookup_field = None

    def get_object(self):
        user = self.request.user

        try:
            user_pref = models.UserPref.objects.get(user_id=user.id)
        except models.UserPref.DoesNotExist:
            user_pref = models.UserPref.objects.create(user=user)

        return user_pref


class ListDogs(generics.RetrieveUpdateAPIView):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        queryset = self.get_queryset()

        if self.kwargs.get('pk') == -1:
            dog = queryset.get(pk=1)
        else:
            dog = self.get_queryset().latest()

        return dog


#kwargs.get is de pk die binnenkomt
#get_object gets a single item