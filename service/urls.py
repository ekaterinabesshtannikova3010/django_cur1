from django.urls import path
from .apps import ServiceConfig
from .views import (RecipientListView, RecipientCreateView, RecipientUpdateView,
                    RecipientDeleteView, HomeView, MailingUpdateView, MailingCreateView, MailingListView,
                    MailingDetailView, MailingDeleteView, SendNewsletterView, MailingStatsView, UserNewsletterView,
                    UserClientView, ManagerDashboardView)
from . import views


app_name = ServiceConfig.name  # Убедитесь, что это возвращает правильное значение

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('recipient/', RecipientListView.as_view(), name='recipient_list'),
    path('recipient/add/', RecipientCreateView.as_view(), name='recipient_add'),
    path('recipient/edit/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_edit'),
    path('recipient/delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),

    path('messages/', views.MessageList.as_view(), name='message_list'),
    path('messages/create/', views.MessageCreate.as_view(), name='message_create'),
    path('messages/<int:pk>/edit/', views.MessageUpdate.as_view(), name='message_edit'),
    path('messages/<int:pk>/delete/', views.MessageDelete.as_view(), name='message_delete'),

    path('mailing', views.MailingListView.as_view(), name='mailing_list'),
    path('mailing/create/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/edit/', views.MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailing/<int:pk>/', views.MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/<int:pk>/delete/',views.MailingDeleteView.as_view(), name='mailing_delete'),
    path('send-newsletter/', SendNewsletterView.as_view(), name='send_newsletter'),
    path('mailing-stats/', MailingStatsView.as_view(), name='mailing_stats'),

    path('user/newsletters/', UserNewsletterView.as_view(), name='user_newsletters'),
    path('user/clients/', UserClientView.as_view(), name='user_clients'),
    path('manager/dashboard/', ManagerDashboardView.as_view(), name='manager_dashboard'),
]
