# スーパーユーザーログイン後確認用
from django.contrib import admin
from .models import ShoppingMemo


@admin.register(ShoppingMemo)
class ShoppingMemoAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "short_content", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("content", "user__username")
    ordering = ("-created_at",)

    def short_content(self, obj):
        return obj.content[:30]

    short_content.short_description = "メモ内容"