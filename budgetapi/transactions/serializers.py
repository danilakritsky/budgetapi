from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
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
