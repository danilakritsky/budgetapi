from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(UserAdmin):
    model = User

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = [
        "id",
        "email",
        "username",
        "subscribed",
        "is_staff",
    ]

    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("subscribed",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("subscribed",)}),
    )


admin.site.register(User, UserAdmin)
