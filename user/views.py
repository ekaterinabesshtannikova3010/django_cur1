from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from .forms import UserRegisterForm, PasswordResetForm
from .models import User

class RegisterView(View):
    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = User(username=username)
        user.set_password(password)
        user.save()
        return redirect('user:login')

class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
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


