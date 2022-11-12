from rest_framework import generics

from .models import Transaction
from .serializers import TransactionSerializer
from budgetapi.permissions import IsAuthenticatedAdminOrAuthor


class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
