from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField(unique=True, blank=False)
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = PhoneNumberField(blank=True)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    phoned = models.BooleanField(default=False)
    SOURCE_CHOICES = (
        ('YouTube', 'YouTube'),
        ('Yandex', 'Yandex'),
        ('Новостная_рассылка', 'Новостная_рассылка'),
    )
    source = models.CharField(choices=SOURCE_CHOICES, max_length=100)
    company = models.CharField(max_length=40)
    phone_company = PhoneNumberField(blank=True)
    email_company = models.EmailField(unique=True, blank=False)
    address_company = models.CharField(max_length=50)
    profile_picture = models.ImageField(blank=True, null=True)
    special_files = models.FileField(blank=True, null=True)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)