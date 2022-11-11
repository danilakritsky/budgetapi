from django.contrib import admin

from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction

    list_display = ["user", "datetime", "category", "amount", "description"]

    list_editable = ["datetime", "category", "amount", "description"]


admin.site.register(Transaction, TransactionAdmin)
