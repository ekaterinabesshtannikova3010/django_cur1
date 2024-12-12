from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .apps import UserConfig
from .views import UserCreateView, ResetPasswordView, PasswordResetDoneView, CampaignStatsView

app_name = UserConfig.name


urlpatterns = [
    path('login/', LoginView.as_view(template_name="user/login.html"), name='login'),
    path('logout/', LogoutView.as_view(template_name="service/base.html"), name= 'logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset-password/done/', PasswordResetDoneView.as_view(), name='reset_password_done'),
    path('campaign-stats/', CampaignStatsView.as_view(), name='campaign_stats'),
]