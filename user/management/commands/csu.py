from django.core.management import BaseCommand
from user.models import User

class Command(BaseCommand):
    """Команда для создания суперпользователя"""
    def handle(self, *args, **options):
        user = User.objects.create(email= "test@yandex.ru")
        user.set_password("1234567/")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
