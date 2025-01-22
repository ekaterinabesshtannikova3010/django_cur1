from django import forms
from .models import Recipient, Message, Mailing


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


class MailingSettingsModeratorForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('status',)


class StyleFormMixin:
    """Стилизация форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
