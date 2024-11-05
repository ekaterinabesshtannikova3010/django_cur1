from django.db import models


class Recipient(models.Model):
    surname = models.CharField(max_length=250, verbose_name='ФИО')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    email = models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')

    def __str__(self):
        return f'{self.surname}'
