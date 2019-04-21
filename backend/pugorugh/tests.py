from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status

from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate


from .models import Dog, UserDog, UserPref

from django.contrib.auth.models import User

from . import serializers
from . import views


class ViewAndModelTest(TestCase):

    def setUp(self):
        """Creates a test object for every model before the tests are ran"""
        self.test_user = User.objects.create_user(
            username='test_that_dog',
            email='test@dog.nl',
            password='password'
        )

        self.test_dog = Dog.objects.create(
            name='Francesca',
            image_filename='picture/perfect/beautiful.jpg',
            breed='Labrador',
            age=72,
            gender='f',
            size='l'
        )

        self.test_user_pref = UserPref.objects.create(
            age='a',
            gender='f',
            size='l',
            user=self.test_user,

        )

        self.test_user_dog = UserDog.objects.create(
            user=self.test_user,
            dog=self.test_dog,
            status='u'
        )

    def test_user_register(self):
        """Tests if a user can be registered """
        factory = APIRequestFactory()
        request = factory.post(reverse('register-user'),
                               {'username': 'Jump', 'password': 'liverpool'})
        view = views.UserRegisterView.as_view()
        response = view(request)

        # one objects gets created in the setup method
        # the other gets created in this method by sending a post request
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, 201)

    def test_already_registerd_user(self):
        """Tests if you can register two users with the same username"""
        factory = APIRequestFactory()
        # Post the same username as creaed in the setup method
        request = factory.post(reverse('register-user'),
                               {'username': 'test_that_dog', 'password': 'liverpool'})

        view = views.UserRegisterView.as_view()
        response = view(request)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, 400)

    def test_user_pref(self):
        """Tests that after login in you can edit your user preferences"""
        factory = APIRequestFactory()
        request = factory.get(reverse('user-pref'))

        force_authenticate(request, user=self.test_user)
        view = views.UserPreferencesView.as_view()
        response = view(request)
        serializer = serializers.UserPrefSerializer(self.test_user_pref)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Compares the serialized data to the response data
        self.assertEqual(response.data, serializer.data)

    def test_dog_creation(self):
        """Tests if dogs can be created"""
        factory = APIRequestFactory()
        # React sends in a -1
        request = factory.get(reverse('undecided-dogs', kwargs={'pk': '-1'}))

        force_authenticate(request, user=self.test_user)

        view = views.ListUndecidedDogsView.as_view()
        response = view(request, pk='-1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # There should be a dog created in the setup method
        self.assertEqual(Dog.objects.count(), 1)
        # Francesca has been created in the setup method
        self.assertEqual(Dog.objects.all().get(pk=1).name, 'Francesca')

    def test_liked_dog_creation(self):
        """Tests if only liked dogs are being displayed"""
        factory = APIRequestFactory()
        request = factory.put(reverse('like-dog', kwargs={'pk': '1'}))

        force_authenticate(request, user=self.test_user)

        view = views.LikedDogsView.as_view()
        response = view(request, pk='1',)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.count(), 1)
        self.assertEqual(UserDog.objects.filter(status='l').count(), 1)
        self.assertEqual(UserDog.objects.filter(status='u').count(), 0)
        self.assertEqual(UserDog.objects.filter(status='d').count(), 0)

    def test_liked_dog_list(self):
        """Tests if a status of a dog can be changed to liked"""
        factory = APIRequestFactory()
        request = factory.get(reverse('liked-dogs', kwargs={'pk': '-1'}))

        # Changing the status of the created dog in the setup method to liked
        disliked_dog = UserDog.objects.filter(dog_id=self.test_dog.pk, user=self.test_user).get()
        disliked_dog.status = 'l'
        disliked_dog.save()

        force_authenticate(request, user=self.test_user)

        view = views.ListDislikedDogsView.as_view()
        response = view(request, pk='-1',)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.count(), 1)
        # checks if the status has been changed
        self.assertEqual(UserDog.objects.filter(status='l').count(), 1)

    def test_disliked_dog_creation(self):
        """Tests if only disliked dogs are being displayed"""
        factory = APIRequestFactory()
        request = factory.put(reverse('dislike-dog', kwargs={'pk': '1'}))

        force_authenticate(request, user=self.test_user)

        view = views.DislikedDogsView.as_view()
        response = view(request, pk='1',)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.count(), 1)
        self.assertEqual(UserDog.objects.filter(status='d').count(), 1)

    def test_disliked_dog_list(self):
        """Tests if a status of a dog can be changed to dislikee"""
        factory = APIRequestFactory()
        request = factory.get(reverse('disliked-dogs', kwargs={'pk': '-1'}))

        disliked_dog = UserDog.objects.filter(dog_id=self.test_dog.pk, user=self.test_user).get()
        disliked_dog.status = 'd'
        disliked_dog.save()

        force_authenticate(request, user=self.test_user)

        view = views.ListDislikedDogsView.as_view()
        response = view(request, pk='-1',)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.count(), 1)
        self.assertEqual(UserDog.objects.filter(status='d').count(), 1)

    def test_undecided_dog_creation(self):
        """Tests if only undecided dogs are being displayed"""
        factory = APIRequestFactory()
        request = factory.put(reverse('undecided-dog', kwargs={'pk': '1'}))

        force_authenticate(request, user=self.test_user)

        view = views.UndecidedDogsView.as_view()
        response = view(request, pk='1',)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.count(), 1)
        self.assertEqual(UserDog.objects.filter(status='u').count(), 1)

    def test_undecided_dog_list(self):
        """Tests if a status of a dog can be changed to undecided"""
        factory = APIRequestFactory()
        request = factory.get(reverse('undecided-dogs', kwargs={'pk': '-1'}))

        force_authenticate(request, user=self.test_user)

        view = views.ListUndecidedDogsView.as_view()
        response = view(request, pk='-1',)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.count(), 1)
        self.assertEqual(UserDog.objects.filter(status='u').count(), 1)
        # Francesca should be by default have the undecided status
        self.assertEqual(Dog.objects.all().get(pk=1).name, 'Francesca')
