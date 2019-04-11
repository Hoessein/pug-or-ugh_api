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


class NextUndecidedDogView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        current_pk = self.kwargs.get('pk')
        undecided_dog = self.get_queryset().filter(pk__gt=current_pk, userdog__status=None).order_by('pk').first()
        # print(self.kwargs.get('poep'))
        return undecided_dog


class LikedDogsView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        current_pk = int(self.kwargs.get('pk'))
        return current_pk

    def put(self, request, pk):
        """Tries to update the UserDog object or returns 404"""
        dog = self.get_object()
        print(dog, "you this is the dog")
        if dog:
            liked_dogs = models.UserDog(status='l', dog_id=dog, user=self.request.user)
            liked_dogs.save()
            print(self.get_queryset().get(pk=dog))
            dogg = self.get_queryset().get(pk=dog)
            serializer = serializers.DogSerializer(dogg)
            return Response(serializer.data)
            # return Response(liked_dogs)


class ListLikedDogsView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        current_pk = self.kwargs.get('pk')
        liked_dogs = self.get_queryset().filter(pk__gt=current_pk, userdog__status='l').order_by('pk').first()
        return liked_dogs


class DislikedDogsView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        current_pk = int(self.kwargs.get('pk'))
        return current_pk

    def put(self, request, pk):
        """Tries to update the UserDog object or returns 404"""
        dog = self.get_object()
        print(dog, "yo this is the dog")
        if dog:
            disliked_dogs = models.UserDog(status='d', dog_id=dog, user=self.request.user)
            disliked_dogs.save()
            print(self.get_queryset().get(pk=dog))
            dogg = self.get_queryset().get(pk=dog)
            serializer = serializers.DogSerializer(dogg)
            return Response(serializer.data)
            # return Response(liked_dogs)


class ListDislikedDogsView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        current_pk = self.kwargs.get('pk')
        liked_dogs = self.get_queryset().filter(pk__gt=current_pk, userdog__status='d').order_by('pk').first()
        return liked_dogs

        #kwargs.get is de pk die binnenkomt
#get_object gets a single item