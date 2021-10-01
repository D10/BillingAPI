from rest_framework import serializers

from .models import CurrentAccount


class CurrentAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrentAccount
        fields = ('name', 'overdraft')

