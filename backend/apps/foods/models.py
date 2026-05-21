from django.db import models
from django.conf import settings


#ユーザーの特定
class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
        
    def __str__(self):
        return self.user.username

# カテゴリ (PREFOODS)
class PreFood(models.Model):
    name = models.CharField("カテゴリー名", max_length=100)
    
    def __str__(self):
        return self.name

    

# 食材
class Food(models.Model):
    #冷蔵庫の特定
    name = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="foods",
    )
    #食材名
    name = models.CharField("食品", max_length=100)
    #カテゴリー
    category = models.ForeignKey(
        PreFood,
        on_delete=models.CASCADE,
        related_name="foods"
    )

    image = models.ImageField(
        "画像",
        upload_to="foods/entry/",
        blank=True,
        null=True,
    )
    #数量
    quantity = models.PositiveIntegerField("数量", default=0)
    #賞味期限
    expiration_date = models.DateField(
        "賞味期限",
        blank=True,
        null=True,
    )

    #期限なし
    no_expiration_date = models.BooleanField("期限なし", default=False)

    #カテゴリー手入力
    custom_category = models.CharField(
        "カテゴリー手入力",
        max_length=50,
        blank=True,
    )

    #作成日時
    created_at = models.DateTimeField(auto_now_add=True)
    #更新日時
    updated_at = models.DateTimeField(auto_now=True)
    


    def __str__(self):
        return self.name



    