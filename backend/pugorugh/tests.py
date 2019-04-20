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
            age='a',
            gender='f',
            size='l'
        )

        self.user_dog = UserDog.objects.create(
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

    def test_liked_dog_creation(self):
        factory = APIRequestFactory()
        request = factory.put(reverse('like-dog', kwargs={'pk': '1'}))

        force_authenticate(request, user=self.test_user)

        view = views.LikedDogsView.as_view()
        response = view(request, pk='1',)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.count(), 1)
        self.assertEqual(UserDog.objects.filter(status='l').count(), 1)

    def test_liked_dog_list(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('liked-dogs', kwargs={'pk': '-1'}))

        disliked_dog = UserDog.objects.filter(dog_id=self.dog.pk, user=self.test_user).get()
        disliked_dog.status = 'l'
        disliked_dog.save()

        force_authenticate(request, user=self.test_user)

        view = views.ListDislikedDogsView.as_view()
        response = view(request, pk='-1',)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.count(), 1)
        self.assertEqual(UserDog.objects.filter(status='l').count(), 1)

    def test_disliked_dog_creation(self):
        factory = APIRequestFactory()
        request = factory.put(reverse('dislike-dog', kwargs={'pk': '1'}))

        force_authenticate(request, user=self.test_user)

        view = views.DislikedDogsView.as_view()
        response = view(request, pk='1',)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.count(), 1)
        self.assertEqual(UserDog.objects.filter(status='d').count(), 1)

    def test_disliked_dog_list(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('disliked-dogs', kwargs={'pk': '-1'}))

        disliked_dog = UserDog.objects.filter(dog_id=self.dog.pk, user=self.test_user).get()
        disliked_dog.status = 'd'
        disliked_dog.save()

        force_authenticate(request, user=self.test_user)

        view = views.ListDislikedDogsView.as_view()
        response = view(request, pk='-1',)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.count(), 1)
        self.assertEqual(UserDog.objects.filter(status='d').count(), 1)


    def test_undecided_dog_creation(self):
        factory = APIRequestFactory()
        request = factory.put(reverse('undecided-dog', kwargs={'pk': '1'}))

        force_authenticate(request, user=self.test_user)

        view = views.UndecidedDogsView.as_view()
        response = view(request, pk='1',)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.count(), 1)
        self.assertEqual(UserDog.objects.filter(status='u').count(), 1)

    def test_undecided_dog_list(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('undecided-dogs', kwargs={'pk': '-1'}))

        force_authenticate(request, user=self.test_user)

        view = views.ListUndecidedDogsView.as_view()
        response = view(request, pk='-1',)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.count(), 1)
        self.assertEqual(UserDog.objects.filter(status='u').count(), 1)
        self.assertEqual(Dog.objects.get(pk=1).name, 'Francesca')
