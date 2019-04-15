from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    MALE = 'm'
    FEMALE = 'f'
    UNKNOWN = 'u'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNKNOWN, 'Unknown'),
    )

    SMALL = 's'
    MEDIUM = 'm'
    LARGE = 'l'
    EXTRA_LARGE = 'xl'
    SIZE_CHOICES = (
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
        (EXTRA_LARGE, 'Extra Large'),
    )

    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255, default="")
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)

    def __str__(self):
        return self.name


class UserDog(models.Model):
    LIKED = 'l'
    DISLIKED = 'd'
    UNDECIDED = 'u'
    STATUS_CHOICES = (
        (LIKED, 'Liked'),
        (DISLIKED, 'Disliked'),
        (UNDECIDED, 'Undecided')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user_id
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)  # dog_id
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=UNDECIDED)

    def __str__(self):
        return self.dog.name


class UserPref(models.Model):
    # BABY = 'b'
    # YOUNG = 'y'
    # ADULT = 'a'
    # SENIOR = 's'
    # AGE_CHOICES = (
    #     (BABY, 'Baby'),
    #     (YOUNG, 'Young'),
    #     (ADULT, 'Adult'),
    #     (SENIOR, 'Senior'),
    # )

    MALE = 'm'
    FEMALE = 'f'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    # SMALL = 's'
    # MEDIUM = 'm'
    # LARGE = 'l'
    # EXTRA_LARGE = 'xl'
    # SIZE_CHOICES = (
    #     (SMALL, 'Small'),
    #     (MEDIUM, 'Medium'),
    #     (LARGE, 'Large'),
    #     (EXTRA_LARGE, 'Extra Large'),
    # )

    user = models.OneToOneField(User)
    age = models.CharField(max_length=1, default='b,y,a,s')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    size = models.CharField(max_length=2, default='s,m,l,xl')

    def __str__(self):
        return self.user.username


