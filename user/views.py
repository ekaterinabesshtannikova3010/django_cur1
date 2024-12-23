import secrets

from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from .forms import PasswordResetForm, RegistrationForm
from .models import User


class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                request.session['user_id'] = user.id
                return redirect('home')
        except User.DoesNotExist:
            pass
        return render(request, 'user/login.html')



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


class RegisterView(View):
    template_name = 'user/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('user:login')

    # def form_valid(self, form):
    #     user = form.save()
    #     user.is_active = False
    #     token = secrets.token_hex(16)
    #     user.token = token
    #     user.save()
    #     host = self.request.get_host()
    #     url = f"http://{host}/users/confirm-registration/{token}/"
    #     send_mail(
    #         subject="Подтверждение регистрации на Perfect Mailing",
    #         message=f"Здравствуйте! Для подтверждения регистрации перейдите по ссылке: {url}",
    #         from_email='dolmatova3010@yandex.ru',
    #         recipient_list=[user.email],
    #     )
    #
    #     messages.success(
    #         self.request,
    #         "Вы успешно зарегистрировались! Проверьте вашу почту для подтверждения регистрации."
    #     )
    #     return super().form_valid(form)
    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        email = request.POST['email']
        raw_password = request.POST['password']
        country = request.POST.get('country', '')

        user = User(email=email, country=country)
        user.set_password(raw_password)
        user.token = user.generate_confirmation_token()
        user.save()

        send_mail(
            'Подтвердите регистрацию',
            f'Пожалуйста, подтвердите вашу регистрацию по следующей ссылке: http://localhost:8000/confirm/{user.token}/',
            'dolmatova3010@yandex.ru',
            [user.email],
            fail_silently=False,
        )
        return HttpResponse("Пожалуйста, проверьте вашу почту для подтверждения регистрации.")

class ConfirmEmailView(View):
    def get(self, request, token):
        email = User.confirm_token(token)
        if email:
            user = User.objects.get(email=email)
            user.is_active = True
            user.token = None  # Очистить токен после подтверждения
            user.save()
            return HttpResponse("Регистрация подтверждена! Вы теперь можете войти.")
        else:
            return HttpResponse("Недействительный или просроченный токен.")

