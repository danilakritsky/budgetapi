from rest_framework import serializers

from .models import Transaction


class TransactionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "user",
            "datetime",
            "category",
            "amount",
            "description"
        )

        model = Transaction

class TransactionAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id', 'user')
        model = Transaction