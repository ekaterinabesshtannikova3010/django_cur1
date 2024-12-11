from django.core.mail import send_mail
from django.views import generic, View
from .forms import MessageForm, RecipientForm, MailingForm
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from .models import Mailing, Message, Recipient

class HomeView(TemplateView):
    template_name = 'service/base.html'


class RecipientListView(ListView):
    model = Recipient
    template_name = 'recipient_list.html'
    context_object_name = 'recipients'

    def recipient_list(request):
        recipients = Recipient.objects.all()
        return render(request, 'service/recipient_list.html', {'recipients': recipients})


class RecipientCreateView(CreateView):
    model = Recipient
    template_name = 'service/recipient_form.html'
    form_class = RecipientForm

    def get_success_url(self):
        return reverse_lazy('service:recipient_list')


class RecipientUpdateView(UpdateView):
    model = Recipient
    template_name = 'service/recipient_form.html'
    form_class = RecipientForm
    success_url = reverse_lazy('service:recipient_list')

    def get_object(self, queryset=None):
        # Переопределяем get_object для добавления логики получения объекта
        return get_object_or_404(Recipient, pk=self.kwargs.get('pk'))


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'service/recipient_confirm_delete.html'
    success_url = reverse_lazy('service:recipient_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Recipient, pk=self.kwargs.get('pk'))


class MessageList(generic.ListView):
    model = Message
    template_name = 'service/message_list.html'
    context_object_name = 'messages'

class MessageCreate(generic.CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'service/message_form.html'
    success_url = reverse_lazy('service:message_list')

class MessageUpdate(generic.UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'service/message_form.html'
    success_url = reverse_lazy('service:message_list')

class MessageDelete(generic.DeleteView):
    model = Message
    template_name = 'service/message_confirm_delete.html'
    success_url = reverse_lazy('service:message_list')


class MailingListView(ListView):
    model = Mailing
    template_name = 'service/mailing_list.html'
    context_object_name = 'mailings'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'service/mailing_form.html'
    success_url = reverse_lazy('service:mailing_list')


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'service/mailing_detail.html'


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'service/mailing_form.html'
    success_url = reverse_lazy('service:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'service/mailing_confirm_delete.html'
    success_url = reverse_lazy('service:mailing_list')




class SendNewsletterView(View):
    template_name = "service/send_newsletter.html"

    def get(self, request):
        mailing = Message.objects.all()
        return render(request, self.template_name, {'messages': mailing})

    def post(self, request, mailing=None):
        mailing_id = request.POST.get('mailing')
        recipients = Recipient.objects.all()

        if mailing_id:
            mailing = Message.objects.get(id=mailing_id)
            for recipient in recipients:
                send_mail(
                    mailing.subject,
                    mailing.body,
                    'from@example.com',
                    [recipient.email],
                    fail_silently=False,
                )
            mailing.success(request, "Рассылка успешно отправлена!")
            return redirect('send_newsletter')
        else:
            mailing.error(request, "Не выбрано сообщение для отправки.")
            return redirect('send_newsletter')


class MailingStatsView(View):
    def get(self, request):
        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(status='Запущена').count()
        unique_recipients = Recipient.objects.distinct().count()

        context = {
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'unique_recipients': unique_recipients,
        }
        return render(request, 'service/mailing_stats.html', context)
