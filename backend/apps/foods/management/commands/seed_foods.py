from django.core.management.base import BaseCommand
from apps.foods.models import PreFood, FoodTemplate


class Command(BaseCommand):
    help = "カテゴリと食品マスターデータを作成"

    def handle(self, *args, **kwargs):
        food_map = {
            "果物": ["りんご", "バナナ", "みかん"],
            "肉": ["牛肉", "豚肉", "鶏肉"],
            "魚": ["サーモン", "マグロ", "イワシ"],
            "飲み物": ["水", "コーラ", "お茶"],
            "野菜": ["キャベツ", "にんじん", "玉ねぎ"],
        }

        created = 0

        for category_name, food_names in food_map.items():
            category, _ = PreFood.objects.get_or_create(name=category_name)

            for food_name in food_names:
                _, was_created = FoodTemplate.objects.get_or_create(
                    name=food_name,
                    category=category,
                )

                if was_created:
                    created += 1

        self.stdout.write(self.style.SUCCESS(f"{created}件作成"))