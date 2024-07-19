from decimal import Decimal

from dirtyfields import DirtyFieldsMixin
from django.core.exceptions import ValidationError
from django.db import models

from djangoProject.signals import recalc_balance


class Wallet(models.Model, DirtyFieldsMixin):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=25, decimal_places=18)

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        dirty_fields = self.get_dirty_fields()
        if "balance" in dirty_fields and self.balance and self.balance < Decimal("0"):
            raise ValidationError(
                "Wallet balance can't be less than zero"
            )
        super().save(*args, **kwargs)


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    wallet = models.ForeignKey(Wallet, related_name="transactions", on_delete=models.CASCADE)
    txid = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=25, decimal_places=18)

    def __str__(self):
        return self.txid

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        recalc_balance.send(
            sender=self.__class__,
            instance=self,
        )
