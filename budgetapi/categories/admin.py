from django.contrib import admin

from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    model = Category

    list_display = ["user", "category_name"]

    list_editable = ["category_name"]


admin.site.register(Category, CategoryAdmin)
