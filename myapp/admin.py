from django.contrib import admin
from .models import Wallet, Transaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'balance')
    search_fields = ('label',)
    ordering = ('id',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'txid', 'amount')
    search_fields = ('txid', 'wallet__label')
    ordering = ('id',)
