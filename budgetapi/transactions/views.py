from categories.models import Category
from django_filters import rest_framework as filters
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from budgetapi.permissions import IsAuthenticatedAdminOrOwner
from django.db.models import F, Subquery, OuterRef

from .filters import CustomOrderingFilter, TransactionFilter
from .models import Transaction
from .serializers import (
    TransactionAdminSerializer,
    TransactionAdminUpdateSerializer,
    TransactionSerializer,
)

from django.db.models import Sum

class TransactionList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedAdminOrOwner,)
    serializer_class = TransactionSerializer
    allowed_methods = ("GET", "POST")
    filter_backends = (
        filters.DjangoFilterBackend,
        CustomOrderingFilter,
    )
    filterset_class = TransactionFilter
    ordering_fields = (
        "date",
        "time",
        "amount",
    )

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return TransactionAdminSerializer

        if self.request.method in permissions.SAFE_METHODS:
            return TransactionAdminSerializer
        return TransactionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Transaction.objects.all()
        return Transaction.objects.filter(user=self.request.user)

    def post(self, request):
        # Check for duplicate categories and inject current user if necessary."""
        if not request.user.is_superuser or not request.data.get("user"):
            request.data["user"] = request.user.id
        category_ids = Category.objects.filter(
            user=self.request.user
        ).values_list("id", flat=True)

        # saves updated model
        serializer = TransactionAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedAdminOrOwner,)
    queryset = Transaction.objects.all()
    allowed_methods = ("GET", "PATCH", "DELETE")

    def get_object(self, pk):
        try:
            obj = Transaction.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Transaction.DoesNotExist:
            raise Http404

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            if self.request.method == "PATCH":
                return TransactionAdminUpdateSerializer
            else:
                return TransactionAdminSerializer

        if self.request.method in permissions.SAFE_METHODS:
            return TransactionAdminSerializer
        return TransactionSerializer

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = self.get_serializer_class()(obj)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        obj = self.get_object(pk)
        if not self.request.user.is_superuser:
            request.data["user"] = request.user.id
        elif not request.data.get("user"):
            request.data["user"] = obj.user.id

        serializer = TransactionAdminSerializer(obj, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TransactionStats(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Transaction.objects.all()
        return Transaction.objects.filter(user=self.request.user)
    
    def get(self, request):
        mode = request.query_params.get('mode')
        if not mode:
            return Response({'message': 'Mode not specified.'})
        else:
            queryset = self.get_queryset()
            if not queryset:
                return Response({'message': 'No transaction found.'})
        if mode == 'balance':
            return Response(
                queryset
                .values('amount')
                .aggregate(current_balance=Sum('amount'))
            )
        if mode == 'categories':
            result = (
                queryset
                .values('category__category_name')
                .annotate(total=Sum('amount'))
                .order_by('-total')
                # rename category field
                .annotate(category=F('category__category_name'))
                .values('category', 'total')
            )
            return Response({
                category['category']: category['total']
                for category in result
            })
        return Response(serializer.data)