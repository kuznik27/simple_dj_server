import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from myapp.models import Wallet, Transaction
from myapp.factories import WalletFactory, TransactionFactory


@pytest.mark.django_db
class TestWalletViewSet:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    def test_wallet_list(self, api_client):
        WalletFactory.create_batch(2)
        url = reverse('wallet-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_wallet_create(self, api_client):
        url = reverse('wallet-list')
        data = {
            "label": "New Wallet",
            "balance": "0.0"
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Wallet.objects.count() == 1
        assert Wallet.objects.get().label == "New Wallet"


@pytest.mark.django_db
class TestTransactionViewSet:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    def test_transaction_list(self, api_client):
        TransactionFactory.create_batch(2)
        url = reverse('transaction-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_transaction_create(self, api_client):
        wallet = WalletFactory()
        url = reverse('transaction-list')
        data = {
            "wallet": wallet.id,
            "txid": "txid1",
            "amount": "50.0"
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Transaction.objects.count() == 1
        assert Transaction.objects.get().txid == "txid1"

    def test_transaction_create_negative_balance(self, api_client):
        wallet = WalletFactory(balance=50.0)
        url = reverse('transaction-list')
        data = {
            "wallet": wallet.id,
            "txid": "txid1",
            "amount": "-100.0"
        }
        with pytest.raises(ValidationError,
                           match="Wallet balance can't be less than zero"):
            api_client.post(url, data, format='json')
