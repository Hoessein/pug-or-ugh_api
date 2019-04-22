from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.response import Response

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
    """Allows users to create a new account"""
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class UserPreferencesView(generics.RetrieveUpdateAPIView):
    """Allows users to filter dog preferences"""
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        try:
            # if the users has preferences saved, it will get the current references
            user_pref = self.get_queryset().get(user_id=self.request.user.pk)
        except ObjectDoesNotExist:
            # if the user has no preferences saved, it will create a new one
            user_pref = self.get_queryset().create(user_id=self.request.user.pk)
        return user_pref

    def put(self, request, *args, **kwargs):
        user_pref = self.get_queryset().get(user_id=self.request.user.pk)

        if request.method == 'PUT':
            # if a put method comes in the preferences will get updated
            # based on the form checkboxes.
            data = request.data
            user_pref.age = data.get('age')
            user_pref.gender = data.get('gender')
            user_pref.size = data.get('size')
            user_pref.save()
        serializer = serializers.UserPrefSerializer(user_pref)
        return Response(serializer.data)


class ListUndecidedDogsView(generics.RetrieveUpdateAPIView):
    """Lists all the dogs who have no/undecided status one by one"""
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        current_pk=self.kwargs.get('pk')
        user_pref = models.UserPref.objects.get(user=self.request.user.pk)

        # if the logged in user has not liked/disliked dogs show them all the dogs based on their preferences
        if not models.UserDog.objects.filter(user_id=self.request.user.pk):
            return models.Dog.objects.filter(
                pk__gt=current_pk,
                size__in=user_pref.size.split(','),
                age__in=age_convert(user_pref.age.split(',')),
                gender__in=user_pref.gender).order_by('pk').first()

        # else filter the dogs based on their preferences and liked/disliked dogs
        else:
            try:
                undecided_dog = models.Dog.objects.filter(
                    pk__gt=current_pk,
                    size__in=user_pref.size.split(','),
                    age__in=age_convert(user_pref.age.split(',')),
                    gender__in=user_pref.gender).exclude(
                    Q(userdog__user_id=self.request.user.pk, userdog__status='d') |
                    Q(userdog__user_id=self.request.user.pk, userdog__status='l')
                   ).order_by(
                    'pk').first()
            except ObjectDoesNotExist:
                raise Http404

            return undecided_dog


class UndecidedDogsView(generics.RetrieveUpdateAPIView):
    """Allows the user to update a dog with an undecided status"""
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        current_pk = int(self.kwargs.get('pk'))
        return current_pk

    def put(self, request, pk):
        dog_pk = self.get_object()
        try:
            # Tries to update with an undecided status first if there is a dog available
            undecided_dog = models.UserDog.objects.filter(dog_id=dog_pk, user_id=self.request.user.pk).get()
            undecided_dog.status = 'u'
            undecided_dog.save()
            # If the dog has no status a new one will be created with an undecided status
        except ObjectDoesNotExist:
            undecided_dog = models.UserDog(status='u', dog_id=dog_pk, user_id=self.request.user.pk)
            undecided_dog.save()

        dog = self.get_queryset().get(pk=dog_pk)
        serializer = serializers.DogSerializer(dog)
        return Response(serializer.data)


class LikedDogsView(generics.RetrieveUpdateAPIView):
    """Allows the user to update a dog with a liked status"""
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        current_pk = int(self.kwargs.get('pk'))
        return current_pk

    def put(self, request, pk):
        dog_pk = self.get_object()
        try:
            # Tries to update with a liked status first if there is a dog available
            liked_dog = models.UserDog.objects.filter(dog_id=dog_pk, user_id=self.request.user.pk).get()
            liked_dog.status = 'l'
            liked_dog.save()
            # If the dog has no status a new one will be created with a liked status
        except ObjectDoesNotExist:
            liked_dog = models.UserDog(status='l', dog_id=dog_pk, user_id=self.request.user.pk)
            liked_dog.save()

        dog = self.get_queryset().get(pk=dog_pk)
        serializer = serializers.DogSerializer(dog)
        return Response(serializer.data)


class ListLikedDogsView(generics.RetrieveUpdateAPIView):
    """Lists all the dogs who have a liked status one by one"""
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        current_pk = self.kwargs.get('pk')
        liked_dogs = self.get_queryset().filter(
            pk__gt=current_pk,
            userdog__status='l',
            userdog__user=self.request.user).order_by('pk').first()
        return liked_dogs


class DislikedDogsView(generics.RetrieveUpdateAPIView):
    """Allows the user to update a dog with a disliked status"""
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        current_pk = int(self.kwargs.get('pk'))
        return current_pk

    def put(self, request, pk):
        dog_pk = self.get_object()
        try:
            # Tries to update with a disliked status first if there is a dog available
            disliked_dog = models.UserDog.objects.filter(dog_id=dog_pk, user_id=self.request.user.pk).get()
            disliked_dog.status = 'd'
            disliked_dog.save()
            # If the dog has no status a new one will be created with a disliked status
        except ObjectDoesNotExist:
            disliked_dog = models.UserDog(status='d', dog_id=dog_pk, user_id=self.request.user.pk)
            disliked_dog.save()

        dog = self.get_queryset().get(pk=dog_pk)
        serializer = serializers.DogSerializer(dog)
        return Response(serializer.data)


class ListDislikedDogsView(generics.RetrieveUpdateAPIView):
    """Lists all the dogs who have a disliked status one by one"""
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        current_pk = self.kwargs.get('pk')
        liked_dogs = self.get_queryset().filter(
            pk__gt=current_pk,
            userdog__status='d',
            userdog__user=self.request.user).order_by('pk').first()
        return liked_dogs
