from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status

from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate


from .models import Dog, UserDog, UserPref

from django.contrib.auth.models import User

from . import serializers
from . import views

class ViewTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            username='test_that_dog',
            email='test@dog.nl',
            password='password'
        )

        self.dog = Dog.objects.create(
            name='Francesca',
            image_filename='pugorugh/static/images/dogs/1.jpg',
            breed='Labrador',
            age=72,
            gender='f',
            size='l'
        )

        self.user_pref = UserPref.objects.create(
            user=self.test_user,
            age='b,y,a,s',
            gender='m,f',
            size='s,m,l,xl'
        )

        UserDog.objects.create(
            user=self.test_user,
            dog=self.dog,
            status='u'
        )


    def test_register_view(self):
        factory = APIRequestFactory()
        request = factory.post(reverse('register-user'), {'username': 'Jump', 'password': 'liverpool',})
        view = views.UserRegisterView.as_view()
        response = view(request)

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, 201)

    def test_user_pref(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('user-pref'))
        force_authenticate(request, user=self.test_user)
        view = views.UserPreferencesView.as_view()
        response = view(request)


        serializer = serializers.UserPrefSerializer(self.user_pref)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_dog_creation(self):
        factory = APIRequestFactory()


        request = factory.get(reverse('undecided-dogs', kwargs={'pk': '-1'}))

        force_authenticate(request, user=self.test_user)

        view = views.ListUndecidedDogsView.as_view()
        response = view(request, pk='-1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.count(), 1)
        self.assertEqual(Dog.objects.get(pk=1).name, 'Francesca')