import factory
from myapp.models import Wallet, Transaction


class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wallet

    label = factory.Faker('word')
    balance = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    wallet = factory.SubFactory(WalletFactory)
    txid = factory.Faker('uuid4')
    amount = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
