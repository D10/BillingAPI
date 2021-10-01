from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db import transaction

from .models import CurrentAccount, Transactions
from .serializers import CurrentAccountSerializer
from .services import response_exception # Ф-ия, которая просто отдает {'success': false}


class Transaction:

    def __init__(self, donor_pk, recipient_pk, transfer_amount):
        self.donor_pk = donor_pk
        self.recipient_pk = recipient_pk
        self.transfer_amount = float(transfer_amount)

    @transaction.atomic
    def make_transaction(self, donor, recipient):
        """Ф-ия, проводящая транзакцию -списывает баланс с донора, начисляет аналогичный баланс реципиенту
        и записыват транзакцию в историю платежей"""
        donor.write_off_balance(self.transfer_amount)
        recipient.add_balace(self.transfer_amount)
        Transactions(donor=donor, recipient=recipient, transfer_amount=self.transfer_amount).save()

    def response_transaction(self):
        """Проводит валидацию данных транзакции и в случае правильности, совершает перевод. Отдает ответ,
        в котором содержится только success с успехом или НЕ успехом транзакции"""
        try:  # Проверяем существование счетов
            donor = CurrentAccount.objects.get(pk=self.donor_pk)
            recipient = CurrentAccount.objects.get(pk=self.recipient_pk)
        except CurrentAccount.DoesNotExist:
            return response_exception()
        if self.transfer_amount < 1:  # Проверка на то, что сумма списания - это положительное число
            return response_exception()
        if donor == recipient:  # Проверка на то, что пользователь не пытается сделать транзакцию самому себе
            return response_exception()
        if donor.overdraft:  # Проверка на то, есть ли у пользователя овердрафт лимит и хватит ли у него денег
            if donor.balance < self.transfer_amount:
                return response_exception()
        self.make_transaction(donor, recipient)
        return Response({'success': True})


class BillingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = CurrentAccount.objects.all()
    serializer_class = CurrentAccountSerializer

    def init_transaction(self):
        """Достаем из тела запроса донора, реципиента, сумму транзакции и возвращаем их"""
        donor_pk = self.request.data['donor']
        recipient_pk = self.request.data['recipient']
        transfer_amount = self.request.data['transfer_amount']
        return donor_pk, recipient_pk, transfer_amount

    def response_balance(self):
        account_id = self.request.data['account_id']
        try:
            account = CurrentAccount.objects.get(pk=account_id)
        except CurrentAccount.DoesNotExist:
            return response_exception()
        return Response({'balance': account.balance})

    @action(detail=False)
    def transactions(self, *args, **kwargs):
        """Инициализирует данные из тела запроса и отправляет полученные данные в класс для свершения
        транзакции, получает от него ответ типа: {'response': true} и перенаправляет его пользователю"""
        donor_pk, recipient_pk, transfer_amount = self.init_transaction()
        post_transaction = Transaction(donor_pk, recipient_pk, transfer_amount)
        response = post_transaction.response_transaction()
        return response

    @action(detail=False)
    def get_account_balance(self, *args, **kwargs):
        """Достаем баланс пользователя, перенаправляет ответ из ф-ии,
        которая проводит валидацию и формирование ответа"""
        account_balance = self.response_balance()
        return account_balance


