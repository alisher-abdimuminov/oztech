from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import UserManager


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, verbose_name="Telefon raqami")
    full_name = models.CharField(max_length=100, verbose_name="Ism")
    image = models.ImageField(upload_to="images/users", null=True, blank=True, verbose_name="Rasm")

    objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "Talaba"
        verbose_name_plural = "Talabalar"


class Contact(models.Model):
    name = models.CharField(max_length=1000)
    phone = models.CharField(max_length=1000)
    telegram = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Date(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey("courses.course", on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    ended = models.DateField()

    def __str__(self):
        return str(self.created)
