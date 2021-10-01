from django.db import models


class CurrentAccount(models.Model):
    name = models.CharField(verbose_name='Название счета', primary_key=True, max_length=256)
    overdraft = models.BooleanField(verbose_name='Овердрафт счета')
    balance = models.FloatField(verbose_name='Баланс счета', default=0.0)

    class Meta:
        verbose_name = 'Текущий счет'
        verbose_name_plural = 'Текущие счета'

    def __str__(self):
        return self.name

    def get_balance(self):
        return self.balance

    def write_off_balance(self, write_off_amount):
        self.balance -= write_off_amount
        self.save()

    def add_balace(self, accrued_balance):
        self.balance += accrued_balance
        self.save()


class Transactions(models.Model):
    donor = models.ForeignKey(CurrentAccount, on_delete=models.PROTECT,
                              verbose_name='Счет донора', related_name='donor')
    recipient = models.ForeignKey(CurrentAccount, on_delete=models.PROTECT,
                                  verbose_name='Счет реципиента', related_name='recipient')
    transfer_amount = models.FloatField(verbose_name='Сумма перевода')

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
