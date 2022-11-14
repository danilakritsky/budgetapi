from django.db import IntegrityError
from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from budgetapi.permissions import IsAuthenticatedAdminOrOwner

from .models import Category
from .serializers import (
    CategoryAdminSerializer,
    CategoryAdminUpdateSerializer,
    CategorySerializer,
)


class CategoryList(generics.ListAPIView):
    permission_classes = (IsAuthenticatedAdminOrOwner,)
    allowed_methods = ("GET", "POST")

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
        # Check for duplicate categories and inject current user if necessary.
        if not request.user.is_superuser or not request.data.get("user"):
            request.data["user"] = request.user.id

        serializer = CategoryAdminSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError:
                raise PermissionDenied({"error": "Category already exists."})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedAdminOrOwner,)
    queryset = Category.objects.all()
    allowed_methods = ("GET", "PATCH", "DELETE")

    def get_object(self, pk):
        try:
            obj = Category.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Category.DoesNotExist:
            raise Http404

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            if self.request.method == "PATCH":
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
            request.data["user"] = request.user.id
        else:
            if not request.data.get("user"):
                request.data["user"] = obj.user.id
            # do not allow creating duplicate categories for another users
            if not request.data.get("category_name"):
                request.data["category_name"] = obj.category_name

        serializer = CategoryAdminSerializer(obj, data=request.data)

        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError:
                raise PermissionDenied({"error": "Category already exists."})
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
