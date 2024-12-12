from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView

from .forms import UserRegisterForm, PasswordResetForm
from .models import User, EmailCampaign


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш сервис'
        message = 'Спасибо, что зарегистрировались в нашем сервисе!'
        from_mail = 'dolmatova3010@yandex.ru'
        recipient_list = [user_email]
        send_mail(subject, message, from_mail, recipient_list)


class ResetPasswordView(FormView):
    template_name = 'user/reset_password.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('user:reset_password_done')  # URL для перенаправления после успешного сброса

    def form_valid(self, form):
        email = form.cleaned_data['email']
        new_password = form.cleaned_data['new_password']

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return super().form_valid(form)  # вызывает метод form_valid родительского класса
        except User.DoesNotExist:
            form.add_error('email', 'Пользователь с таким адресом электронной почты не найден.')
            return self.form_invalid(form)  # возвращает недействительную форму


class PasswordResetDoneView(View):
    def get(self, request):
        return render(request, 'user/reset_password_done.html')



class CampaignStatsView(LoginRequiredMixin, TemplateView):
    template_name = 'user/campaign_stats.html'  # Укажите ваш шаблон здесь

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем количество успешных и неуспешных рассылок
        stats = EmailCampaign.objects.values('status').annotate(count=Count('id'))

        success_count = next((item['count'] for item in stats if item['status'] == 'success'), 0)
        failed_count = next((item['count'] for item in stats if item['status'] == 'failed'), 0)

        # Общее количество отправленных сообщений
        total_count = success_count + failed_count

        # Добавляем данные в контекст
        context['success_count'] = success_count
        context['failed_count'] = failed_count
        context['total_count'] = total_count

        return context