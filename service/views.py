# from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views import generic, View

from .forms import MessageForm, RecipientForm, MailingForm
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from .models import Mailing, Message, Recipient, MailingAttempts


class HomeView(TemplateView):
    template_name = 'service/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailings'] = Mailing.objects.all()
        context["active_mailings"] = Mailing.objects.filter(status='Запущена').count()
        context["unique_recipients"] = Recipient.objects.distinct().count()
        context["total_mailings"] = Mailing.objects.count()
        return context


class RecipientListView(ListView):
    model = Recipient
    template_name = 'recipient_list.html'
    context_object_name = 'recipients'

    def recipient_list(request):
        recipients = Recipient.objects.all()
        return render(request, 'service/recipient_list.html', {'recipients': recipients})


class RecipientCreateView(CreateView):
    """
        Создание пользователя.
    """
    model = Recipient
    template_name = 'service/recipient_form.html'
    form_class = RecipientForm

    def get_success_url(self):
        return reverse_lazy('service:recipient_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(UpdateView):
    model = Recipient
    template_name = 'service/recipient_form.html'
    form_class = RecipientForm
    success_url = reverse_lazy('service:recipient_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Recipient, pk=self.kwargs.get('pk'))

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.is_staff


class RecipientDeleteView(DeleteView):
    """
    Удаление пользователя.
    """
    model = Recipient
    template_name = 'service/recipient_confirm_delete.html'
    success_url = reverse_lazy('service:recipient_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Recipient, pk=self.kwargs.get('pk'))

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.is_staff


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

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.is_staff


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

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.is_staff


class SendNewsletterView(View):
    template_name = "service/send_newsletter.html"

    def get(self, request):
        mailing = Message.objects.all()
        return render(request, self.template_name, {'messages': mailing})

    def post(self, request, mailing=None):
        mailing_id = request.POST.get('mailing')
        recipients = Recipient.objects.filter(user=request.user)

        if mailing_id:
            mailing = Message.objects.get(id=mailing_id)
            for recipient in recipients:
                send_mail(
                    mailing.subject,
                    mailing.body,
                    'dolmatova3010@yandex.ru',
                    [recipient.email],
                    fail_silently=False,
                )
            mailing.success(request, "Рассылка успешно отправлена!")
            return redirect('service:send_newsletter')
        else:
            mailing.error(request, "Не выбрано сообщение для отправки.")
            return redirect('service:send_newsletter')


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


class MailingAttemptController(View):
    def post(self, request, mailing_id):
        mailing = get_object_or_404(Mailing, id=mailing_id)
        recipients = mailing.recipients.all()
        for recipient in recipients:
            try:
                response = send_mail(mailing.message.subject, mailing.message.body, 'dolmatova3010@yandex.ru',
                                     [recipient.email])
                MailingAttempts.objects.create(
                    mailing=mailing,
                    status='Успешно',
                    server_response=str(response)
                )
            except Exception as e:
                MailingAttempts.objects.create(
                    mailing=mailing,
                    status='Не успешно',
                    server_response=str(e)
                )
        return HttpResponse("Попытки рассылки сохранены.")

    def get(self, request, mailing_id):
        mailing_attempts = MailingAttempts.objects.filter(mailing_id=mailing_id)
        return render(request, 'service/mailing_attempts.html',
                      {'mailing_attempts': mailing_attempts})
