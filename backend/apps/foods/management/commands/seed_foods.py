from django.core.management.base import BaseCommand
from apps.foods.models import PreFood, Food
import random

class Command(BaseCommand):
    help = "カテゴリ + 食材を自動生成"

    def handle(self, *args, **kwargs):
        #　カテゴリ
        categories = ["果物", "肉", "野菜", "魚", "飲み物"]

        category_objs = []
        for name in categories:
            obj, _ = PreFood.objects.get_or_create(name=name)
            category_objs.append(obj)

        # 食材候補
        food_names = [
            "りんご", "バナナ", "みかん", "ぶどう", "いちご",
            "牛肉", "豚肉", "鶏肉",
            "サーモン", "マグロ", "イワシ",
            "水", "コーラ", "お茶", "コーヒー"
        ]

        created_count = 0

        for i in range(100):
            name = random.choice(food_names) + f"_{i}"
            category = random.choice(category_objs)

            Food.objects.create(
                name=name,
                category=category
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"{created_count}件の食材を作成しました！"))