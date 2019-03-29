from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNKNOWN, 'Unknown'),
    )

    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    EXTRA_LARGE = 'XL'
    SIZE_CHOICES = (
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
        (EXTRA_LARGE, 'Extra Large'),
    )

    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)

    def __str__(self):
        return self.name


class UserDog(models.Model):
    LIKED = 'l'
    DISLIKED = 'd'
    STATUS_CHOICES = (
        (LIKED, 'Liked'),
        (DISLIKED, 'Disliked'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)


class UserPref(models.Model):
    BABY = 'b'
    YOUNG = 'y'
    ADULT = 'a'
    SENIOR = 's'
    AGE_CHOICES = (
        (BABY, 'Baby'),
        (YOUNG, 'Young'),
        (ADULT, 'Adult'),
        (SENIOR, 'Senior'),
    )

    MALE = 'm'
    FEMALE = 'f'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    EXTRA_LARGE = 'XL'
    SIZE_CHOICES = (
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
        (EXTRA_LARGE, 'Extra Large'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=1, choices=AGE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)

    def __str__(self):
        return self.user.username
