from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError

from django.http import Http404
from rest_framework import status

from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializer, CategoryAdminSerializer, CategoryAdminUpdateSerializer
from .permissions import IsAuthenticatedAdminOrOwner


class CategoryList(generics.ListAPIView):
    permission_classes = (
        IsAuthenticatedAdminOrOwner,
    )
    allowed_methods = ('GET', 'POST')
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

    
    def post(self, request, format=None):
        # Check for duplicate categories and inject current user if necessary."""
        if not request.user.is_superuser:
            category = Category.objects.filter(
                user=request.user.id,
                category_name=request.data.get('category_name')
            )
            # current user can only create categories for himself  
            request.data['user'] = request.user.id

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
        serializer = CategoryAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedAdminOrOwner,)
    queryset = Category.objects.all()
    allowed_methods = ('GET', 'PATCH', 'DELETE')

    def get_object(self, pk):
        try:
            obj = Category.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Category.DoesNotExist:
            raise Http404

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            if self.request.method == 'PATCH':
                return CategoryAdminUpdateSerializer
            else:
                return CategoryAdminSerializer

        if self.request.method in permissions.SAFE_METHODS:
            return CategoryAdminSerializer
        return CategorySerializer

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = self.get_serializer_class()(obj)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        obj = self.get_object(pk)   
        if not self.request.user.is_superuser:
            request.data['user'] = request.user.id
        else:
            if not request.data.get('user'):
                request.data['user'] = obj.user.id
            # do not allow creating duplicate categories for another users
            
            if not request.data.get('category_name'):
                request.data['category_name'] = obj.category_name
            else:
                category = Category.objects.get(
                    # admin user can access every user's category by using the requests payload
                    user=self.request.data.get('user'),
                    category_name=self.request.data.get('category_name')
                )

                if all([
                    category,
                    category.user.id == request.data['user'],
                    # if current user is not the owner
                    request.data['user'] != obj.user.id
                ]):
                    raise ValidationError(
                        {'error': 'Category already exists.'}
                    )
        # use separate serializer to return all fields
        serializer = CategoryAdminSerializer(
            obj,
            data=request.data
        )
            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        