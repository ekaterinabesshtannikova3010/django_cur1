from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from .models import Recipient
from .forms import RecipientForm

# class RecipientListView(View):
#     def get(self, request):
#         recipient = Recipient.objects.all()
#         return render(request, 'recipient/recipient_list.html', {'recipient': recipient})
#
# class RecipientCreateView(View):
#     def get(self, request):
#         form = RecipientForm()
#         return render(request, 'recipient/recipient_form.html', {'form': form})
#
#     def post(self, request):
#         form = RecipientForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('recipient_list')
#         return render(request, 'recipient/recipient_form.html', {'form': form})
#
# class RecipientUpdateView(View):
#     def get(self, request, pk):
#         recipient = get_object_or_404(Recipient, pk=pk)
#         form = RecipientForm(instance=recipient)
#         return render(request, 'recipient/recipient_form.html', {'form': form})
#
#     def post(self, request, pk):
#         recipient = get_object_or_404(Recipient, pk=pk)
#         form = RecipientForm(request.POST, instance=recipient)
#         if form.is_valid():
#             form.save()
#             return redirect('recipient_list')
#         return render(request, 'recipient/recipient_form.html', {'form': form})
#
# class RecipientDeleteView(View):
#     def get(self, request, pk):
#         recipient = get_object_or_404(Recipient, pk=pk)
#         return render(request, 'recipient/recipient_confirm_delete.html', {'recipient': recipient})
#
#     def post(self, request, pk):
#         recipient = get_object_or_404(Recipient, pk=pk)
#         recipient.delete()
#         return redirect('recipient_list')
class HomeView(TemplateView):
    template_name = 'service/base.html'


class RecipientListView(View):

    def recipient_list(request):
        recipients = Recipient.objects.all()
        return render(request, 'recipient_list.html', {'recipients': recipients})

class RecipientCreateView(View):

    def recipient_create(request):
        if request.method == "POST":
            form = RecipientForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('recipient_list')
        else:
            form = RecipientForm()
        return render(request, 'recipient_form.html', {'form': form})


class RecipientUpdateView(View):
    def recipient_update(request, pk):
        recipient = get_object_or_404(Recipient, pk=pk)
        if request.method == "POST":
            form = RecipientForm(request.POST, instance=recipient)
            if form.is_valid():
                form.save()
                return redirect('recipient_list')
        else:
            form = RecipientForm(instance=recipient)
        return render(request, 'recipient_form.html', {'form': form})

class RecipientDeleteView(View):
    def recipient_delete(request, pk):
        recipient = get_object_or_404(Recipient, pk=pk)
        if request.method == "POST":
            recipient.delete()
            return redirect('recipient_list')
        return render(request, 'recipient_confirm_delete.html', {'recipient': recipient})
