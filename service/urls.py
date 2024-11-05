# from django.urls import path
# from service.apps import ServiceConfig
# from service.views import RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView
#
#
# app_name = ServiceConfig.name
#
# urlpatterns = [
#     path('recipient/', RecipientListView.as_view(), name='recipient_list'),
#     path('recipient/add/', RecipientCreateView.as_view(), name='recipient_add'),
#     path('recipient/edit/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_edit'),
#     path('recipient/delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),
# ]
from django.urls import path
from .apps import ServiceConfig  # Убедитесь, что импортируете из текущего приложения
from .views import RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView, HomeView

app_name = ServiceConfig.name  # Убедитесь, что это возвращает правильное значение

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('recipient/', RecipientListView.as_view(), name='recipient_list'),
    path('recipient/add/', RecipientCreateView.as_view(), name='recipient_add'),
    path('recipient/edit/<int:pk>/', RecipientUpdateView.as_view(), name='recipient_edit'),
    path('recipient/delete/<int:pk>/', RecipientDeleteView.as_view(), name='recipient_delete'),
]