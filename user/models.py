from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email

    class Meta():
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class EmailCampaign(models.Model):
    status_choices = (
        ('success', 'Успешно'),
        ('failed', 'Неуспешно'),
    )

    status = models.CharField(max_length=10, choices=status_choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.status} - {self.created_at}"