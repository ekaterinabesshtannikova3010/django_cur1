import pytz
from django.db import models
from datetime import datetime
from config import settings
from user.models import User


class Recipient(models.Model):
    objects = None
    surname = models.CharField(max_length=250, verbose_name='ФИО')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    email = models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')

    def __str__(self):
        return f'{self.surname}'


class Message(models.Model):
    objects = None
    subject = models.CharField(max_length=255)  # Тема письма
    body = models.TextField()  # Тело письма

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    objects = None
    first_sent_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена'),
    ])
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)

    def __str__(self):
        return f"Рассылка: {self.status} - {self.message.body[:20]}"

    def save(self, *args, **kwargs):
        zone = pytz.timezone(settings.TIME_ZONE)
        if self.finished_at and self.finished_at < datetime.now(zone):
            self.status = 'Завершена'
        elif self.first_sent_at:
            self.status = 'Запущена'
        super().save(*args, **kwargs)


class MailingAttempt(models.Model):
    attempt_time = models.DateTimeField(auto_now_add=True)  # Дата и время попытки
    status = models.CharField(max_length=10, choices=[  # Статус
        ('Успешно', 'Успешно'),
        ('Не успешно', 'Не успешно'),
    ])
    server_response = models.TextField()  # Ответ почтового сервера
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    def __str__(self):
        return f"Попытка рассылки: {self.status} - {self.attempt_time}"




class SendAttempt(models.Model):
    STATUS_CHOICES = [
        ('Успешно', 'Успешно'),
        ('Не успешно', 'Не успешно'),
    ]
    attempt_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField()
    campaign = models.ForeignKey(Mailing, on_delete=models.CASCADE)


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

class Newsletter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()