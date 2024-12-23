from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from itsdangerous import URLSafeTimedSerializer, BadSignature
from django import forms

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    country = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    token = models.CharField(max_length=100, verbose_name="token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def set_password(self, raw_password):
        """Сохраняет пароль в зашифрованном виде."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Проверяет, совпадает ли введённый пароль с зашифрованным."""
        return check_password(raw_password, self.password)

    def generate_confirmation_token(self):
        serializer = URLSafeTimedSerializer('secret-key')
        return serializer.dumps(self.email, salt='email-confirm')

    @staticmethod
    def confirm_token(token):
        serializer = URLSafeTimedSerializer('secret-key')
        try:
            email = serializer.loads(token, salt='email-confirm', max_age=3600)
        except BadSignature:
            return False
        return email

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
