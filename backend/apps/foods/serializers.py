from rest_framework import serializers
from .models import Food, PreFood

class PreFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreFood
        fields = ["id", "name"]


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ["id", "name", "category"]
