from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer, TransactionAdminSerializer, TransactionAdminUpdateSerializer
from budgetapi.permissions import IsAuthenticatedAdminOrOwner
from rest_framework.exceptions import PermissionDenied
from categories.models import Category

class TransactionList(generics.ListCreateAPIView):
    permission_classes = (
        IsAuthenticatedAdminOrOwner,
    )
    serializer_class = TransactionSerializer
    allowed_methods = ('GET', 'POST')

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
        if not request.user.is_superuser:
            request.data['user'] = request.user.id
            category_ids = Category.objects.filter(
                user=self.request.user
            ).values_list('id', flat=True)
            # current user can only create categories for himself

        else:
            if not request.data.get('user'):
                request.data['user'] = request.user.id
            category = Category.objects.filter(
                # admin user can access every user's category by using the requests payload
                user=request.data.get('user') or request.user.id,
                category_name=request.data.get('category_name')
            )

        # no duplicates
        if category.exists():
            raise ValidationError({'error': 'Category already exists.'})
        
        # saves updated model
        serializer = TransactionAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

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
