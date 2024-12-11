from django.core.management.base import BaseCommand
from service.models import Recipient, Message
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Send newsletters to all recipients'

    def handle(self, *args, **kwargs):
        messages = Message.objects.all()
        for message in messages:
            recipients = Recipient.objects.all()
            for recipient in recipients:
                send_mail(
                    message.subject,
                    message.body,
                    'dolmatova3010@yandex.ru',
                    [recipient.email],
                    fail_silently=False,
                )
        self.stdout.write(self.style.SUCCESS('Рассылка успешно отправлена!'))