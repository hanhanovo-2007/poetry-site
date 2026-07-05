from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(Group)

class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "email", "date_joined", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "date_joined")
    search_fields = ("username", "email")
    ordering = ("-date_joined",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("个人信息", {"fields": ("first_name", "last_name", "email")}),
        ("权限", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("重要日期", {"fields": ("last_login", "date_joined")}),
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
