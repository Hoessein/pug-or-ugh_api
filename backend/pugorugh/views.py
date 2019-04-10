from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


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


class NextDogView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        # queryset = models.Dog.objects.get(pk=1)
        # # print(self.queryset)
        # pk = int(self.kwargs.get('pk'))
        # pk += 1
        # print(pk)
        # return self.get_queryset().get_next_by_id()


        p = self.kwargs.get('pk')

        m = self.get_queryset().filter(pk__gt=p).order_by('pk').first()
        return m

        #kwargs.get is de pk die binnenkomt
#get_object gets a single item