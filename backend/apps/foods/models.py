from django.db import models

# カテゴリ　(PREFOODS)
class PreFood(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    

# 食材
class Food(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        PreFood,
        on_delete=models.CASCADE,
        related_name="foods"
    )
    name = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to="foods/entry/"
        blank=True,
        null=True,
    )
    quantity = models.PositiveIntegerField("数量")
    expiration_date = models.DateField(
        "賞味期限",
        blank=True,
        null=True,
    )
    no_expiration_date = models.DateField("期限なし", default=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name = "カテゴリー"
    )

    custom_category = models.CharField(
        "カテゴリー手入力",
        max_length=50,
        blank=True,
        )


    def __str__(self):
        return self.name


    