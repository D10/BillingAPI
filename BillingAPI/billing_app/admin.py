from django.contrib import admin

from .models import CurrentAccount, Transactions


@admin.register(CurrentAccount)
class CurrentAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance', 'overdraft')


@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'donor', 'recipient', 'transfer_amount')
