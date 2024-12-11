from django.contrib import admin
from .models import Recipient, Mailing


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname')
    search_fields = ('surname', 'comment')


admin.site.register(Mailing)