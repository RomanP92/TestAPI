import requests
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.text import Truncator
from bs4 import BeautifulSoup


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=False):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.is_active = is_active
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, is_active=True):
        user = self.create_user(
            email=email,
            password=password,
            is_active=is_active,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUserModel(AbstractUser):
    email = models.EmailField('Email', unique=True)
    # username = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class CollectionModel(models.Model):
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class LinkModel(models.Model):
    TYPE_CHOICES = (
        ('website', 'Website'),
        ('book', 'Book'),
        ('article', 'Article'),
        ('music', 'Music'),
        ('video', 'Video'),
    )
    collection = models.ForeignKey(CollectionModel, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    link_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='website')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('author', 'url'),)

    def save(self, *args, **kwargs):
        self.fetch_data()
        super().save(*args, **kwargs)

    def fetch_data(self):
        try:
            response = requests.get(str(self.url))
            soup = BeautifulSoup(response.text, 'html.parser')

            og_title = soup.find('meta', property='og:title')
            og_description = soup.find('meta', property='og:description')
            og_image = soup.find('meta', property='og:image')
            og_type = soup.find('meta', property='og:type')

            if og_title:
                self.title = og_title['content']
            else:
                self.title = soup.title.string if soup.title else "Untitled"

            if og_description:
                self.description = og_description['content']
            else:
                meta_description = soup.find('meta', attrs={'name': 'description'})
                self.description = meta_description['content'] if meta_description else ""

            if og_image:
                self.image = og_image['content']

            if og_type:
                self.link_type = og_type['content']
            else:
                self.link_type = 'website'

        except Exception as e:
            print("Error fetching data:", e)

    def __str__(self):
        return Truncator(self.title).chars(50)
