from rest_framework import generics
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer
from categories.permissions import IsAuthenticatedAdminOrOwner
from rest_framework.exceptions import PermissionDenied
from categories.models import Category

class TransactionList(generics.ListCreateAPIView):
    permission_classes = (
        IsAuthenticatedAdminOrOwner,
    )
    serializer_class = TransactionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Transaction.objects.all()
        return Transaction.objects.filter(user=self.request.user)
    
    def post(self, request):
        user_categories_ids = Category.objects.filter(
            user=self.request.user
        ).values_list('id', flat=True)
        if (category_id := request.data['category']) not in user_categories_ids:
            raise PermissionDenied({'message': f'Invalid category id {category_id}.'})
        if any([
            request.data['user'] == self.request.user.id,
            request.user.is_superuser
        ]) and request.data['category'] in user_categories_ids:
            serializer = TransactionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        raise PermissionDenied()


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedAdminOrOwner,)
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
