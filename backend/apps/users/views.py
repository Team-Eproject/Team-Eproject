from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user) # セッションに保存
            return Response({"message": "ログインしました"})
        
        return Response(
            {"error": "ユーザー名かパスワードが違います"},
            status=status.HTTP_400_BAD_REQUEST
        )
