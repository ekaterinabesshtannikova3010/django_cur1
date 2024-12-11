from django import forms
from .models import Recipient, Message, Mailing, SendAttempt

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'surname', 'comment']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['first_sent_at', 'finished_at', 'status', 'message', 'recipients']
        widgets = {
            'first_sent_at': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'finished_at': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),

            'message': forms.Select(attrs={'class': 'form-control'}),
            'recipients': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class SendAttemptForm(forms.ModelForm):
    class Meta:
        model = SendAttempt
        fields = ['attempt_time', 'server_response', 'status', 'campaign']
