from __future__ import annotations

from decimal import Decimal

from django.db.models import Sum
from django.dispatch import receiver

from djangoProject.signals import recalc_balance
from myapp.models import Transaction


@receiver(recalc_balance, sender=Transaction)
def recalc_balance_for_wallet(sender, instance: Transaction, **kwargs):
    wallet = instance.wallet
    balance = wallet.transactions.all().aggregate(balance=Sum("amount"))["balance"]
    wallet.balance = balance or Decimal("0")
    wallet.save()
