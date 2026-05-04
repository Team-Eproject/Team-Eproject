from django.db import models

# カテゴリ　(PREFOODS)
class PreFood(models.Models):
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

    def __str__(self):
        return self.name