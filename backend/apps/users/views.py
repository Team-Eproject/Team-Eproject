from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import SignupSerializer

# サインアップAPI 追加 byかかの
class SignupView(APIView):
    # ログインしていない人でもこのAPIを使えるようにする
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "ユーザー登録が完了しました。",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

# ログインAPI
class LoginView(APIView):
    # ログインしていない人でもこのAPIを使えるようにする
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            request,
            username=username, password=password)

        if user is not None:
            login(request, user) # セッションに保存
            return Response({"message": "ログインしました"})
        
        return Response(
            {"error": "ユーザー名かパスワードが違います"},
            status=status.HTTP_400_BAD_REQUEST
        )

# ログアウトAPI
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "ログアウトしました"})