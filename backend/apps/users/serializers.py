# 認証処理に必要なので作りました byかかの
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        # create_user()はDjangoがパスワードをハッシュ化して保存してくれる
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user