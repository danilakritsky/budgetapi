from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Category
from .serializers import CategorySerializer, CategoryAdminSerializer, CategoryAdminUpdateSerializer
from .permissions import IsAuthenticatedAdminOrOwner


class CategoryList(generics.ListCreateAPIView):
    permission_classes = (
        IsAuthenticatedAdminOrOwner,
    )

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return CategoryAdminSerializer

        if self.request.method in permissions.SAFE_METHODS:
            return CategoryAdminSerializer
        return CategorySerializer


    def get_queryset(self):
        if self.request.user.is_superuser:
            return Category.objects.all()
        return Category.objects.filter(user=self.request.user)

    
    def perform_create(self, serializer):
        """Check for duplicate categories and inject current user if necessary."""
        if not self.request.user.is_superuser:
            # user can access his categories by using request.user
            category = Category.objects.filter(
                user=self.request.user,
                category_name=self.request.data.get('category_name')
            )
            
        else:
            category = Category.objects.filter(
                # admin user can access every user's category by using the requests payload
                user=self.request.data.get('user'),
                category_name=self.request.data.get('category_name')
            )

        # no duplicates
        if category.exists():
            raise ValidationError({'error': 'Category already exists.'})
        
        # saves updated model
        serializer.save(user=(user := self.request.user))
        



class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedAdminOrOwner,)
    queryset = Category.objects.all()
    
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            if self.request.method in ('PUT', 'PATCH'):
                return CategoryAdminUpdateSerializer
            else:
                return CategoryAdminSerializer

        if self.request.method in permissions.SAFE_METHODS:
            return CategoryAdminSerializer
        return CategorySerializer


    def perform_update(self, serializer):
        """Check if update will create a duplicate.""" 
        if self.request.user.is_superuser:
            category = Category.objects.filter(
                # admin user can access every user's category by using the requests payload
                user=self.request.data.get('user'),
                category_name=self.request.data.get('category_name')
            )

            # no duplicates
            if category.exists():
                raise ValidationError({'error': 'Category already exists.'})
        serializer.save()
        