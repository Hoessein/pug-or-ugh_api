from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from django.db.models import Q


from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

from . import serializers
from . import models

b = [x for x in range(0, 15)]
y = [x for x in range(15, 35)]
a = [x for x in range(35, 90)]
s = [x for x in range(90, 9999)]

all_together = []


def age_convert(user_pref_age):
    if 'b' in user_pref_age:
        all_together.extend(b)
    if 'y' in user_pref_age:
        all_together.extend(y)
    if 'a' in user_pref_age:
        all_together.extend(a)
    if 's' in user_pref_age:
        all_together.extend(s)

    return all_together


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class UserPreferencesView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        try:
            user_pref = self.get_queryset().get(user_id=self.request.user.pk)
        except ObjectDoesNotExist:
            user_pref = self.get_queryset().create(user_id=self.request.user.pk)
        return user_pref

    def put(self, request, *args, **kwargs):
        user_pref = self.get_queryset().get(user_id=self.request.user.pk)

        if request.method == 'PUT':
            data = request.data
            user_pref.age = data.get('age')
            user_pref.gender = data.get('gender')
            user_pref.size = data.get('size')
            user_pref.save()
        serializer = serializers.UserPrefSerializer(user_pref)
        return Response(serializer.data)


class ListUndecidedDogsView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        current_pk=self.kwargs.get('pk')
        print(current_pk)
        user_pref = models.UserPref.objects.get(user=self.request.user.pk)

        if not models.UserDog.objects.filter(user_id=self.request.user.pk):
            return models.Dog.objects.filter(pk__gt=current_pk).order_by('pk').first()
        else:
            try:
                undecided_dog = self.get_queryset().filter(
                    pk__gt=current_pk,
                    size__in=user_pref.size.split(','),
                    age__in=age_convert(user_pref.age.split(',')),
                    gender__in=user_pref.gender).exclude(
                    Q(userdog__status__contains='d')).exclude(Q(userdog__status__contains='l')).order_by(
                    'pk').first()
            except ObjectDoesNotExist:
                raise Http404

            return undecided_dog


class UndecidedDogsView(generics.RetrieveUpdateAPIView):
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

        try:
            undecided_dog = models.UserDog.objects.filter(dog_id=dog, user=self.request.user).get()
            undecided_dog.status = 'u'
            undecided_dog.save()
        except ObjectDoesNotExist:
            undecided_dog = models.UserDog(status='u', dog_id=dog, user=self.request.user)
            undecided_dog.save()

        dogg = self.get_queryset().get(pk=dog)
        serializer = serializers.DogSerializer(dogg)
        return Response(serializer.data)


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
        print(dog, "yo this is the dog")
        try:
            liked_dog = models.UserDog.objects.filter(dog_id=dog, user=self.request.user).get()
            liked_dog.status = 'l'
            liked_dog.save()
        except ObjectDoesNotExist:
            liked_dog = models.UserDog(status='l', dog_id=dog, user=self.request.user)
            liked_dog.save()

        dogg = self.get_queryset().get(pk=dog)
        serializer = serializers.DogSerializer(dogg)
        return Response(serializer.data)


class ListLikedDogsView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        current_pk = self.kwargs.get('pk')
        liked_dogs = self.get_queryset().filter(pk__gt=current_pk, userdog__status='l', userdog__user=self.request.user).order_by('pk').first()
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
        try:
            disliked_dog = models.UserDog.objects.filter(dog_id=dog, user=self.request.user).get()
            disliked_dog.status = 'd'
            disliked_dog.save()
        except ObjectDoesNotExist:
            disliked_dog = models.UserDog(status='d', dog_id=dog, user=self.request.user)
            disliked_dog.save()

        dogg = self.get_queryset().get(pk=dog)
        serializer = serializers.DogSerializer(dogg)
        return Response(serializer.data)


class ListDislikedDogsView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        current_pk = self.kwargs.get('pk')
        liked_dogs = self.get_queryset().filter(pk__gt=current_pk, userdog__status='d', userdog__user=self.request.user).order_by('pk').first()
        return liked_dogs

#kwargs.get is de pk die binnenkomt
#get_object gets a single item