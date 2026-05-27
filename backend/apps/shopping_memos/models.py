from django.conf import settings
from django.db import models


class ShoppingMemo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shopping_memos",
        verbose_name="ユーザー",
    )

# メモ本文なので、文字数制限のゆるいTextField
    content = models.TextField(
        verbose_name="メモ内容",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="作成日時",
    )

# 更新するたびに自動で日時が更新
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新日時",
    )

    class Meta:
        db_table = "shopping_memos"
        verbose_name = "買い物メモ"
        verbose_name_plural = "買い物メモ"
        ordering = ["-created_at"]

    def __str__(self):
        return self.content[:20]