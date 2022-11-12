from rest_framework import serializers

from .models import Category


class CategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "user",
            "category_name",
        )

        model = Category


class CategoryAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id', 'user')
        model = Category
