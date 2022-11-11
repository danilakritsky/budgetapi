from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Category
from .serializers import CategorySerializer
from .permissions import IsAuthor

class CategoryList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(user=user)
    
    def post(self, request):
        if request.data['user'] == self.request.user.id:
            return Response(request.data)
        return Response({})

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthor,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
