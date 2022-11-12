from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Category
from .serializers import CategorySerializer
from .permissions import IsAuthenticatedAdminOrAuthor

class CategoryList(generics.ListCreateAPIView):
    permission_classes = (
        IsAuthenticatedAdminOrAuthor,
    )
    serializer_class = CategorySerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Category.objects.all()
        return Category.objects.filter(user=self.request.user)
    
    def post(self, request):
        if (request.data['user'] == self.request.user.id) or (
            request.user.is_superuser
        ):
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        raise PermissionDenied()


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedAdminOrAuthor,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
