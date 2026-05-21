from django.core.management.base import BaseCommand
from apps.foods.models import PreFood, Food
import random

class Command(BaseCommand):
    help = "初期データ作成"

    def handle(self, *args, **kwargs):
        if PreFood.objects.exists():

            self.stdout.write("skip seed")
            return

        categories = ["果物", "肉", "野菜", "魚", "飲み物"]

        category_objs = []
        for name in categories:
            obj, _ = PreFood.objects.get_or_create(name=name)
            category_objs.append(obj)

        food_map = {
            "果物": ["りんご", "バナナ", "みかん"],
            "肉": ["牛肉", "豚肉", "鶏肉"],
            "魚": ["サーモン", "マグロ", "イワシ"],
            "飲み物": ["水", "コーラ", "お茶"],
            "野菜": ["キャベツ", "にんじん", "玉ねぎ"],
        }

        created = 0

        for category in category_objs:
            for name in food_map[category.name]:
                obj, c = Food.objects.get_or_create(
                    name=name,
                    category=category
                )
                if c:
                    created += 1

        self.stdout.write(self.style.SUCCESS(f"{created}件作成"))