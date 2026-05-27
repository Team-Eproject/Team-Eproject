from django.urls import path
from . import views

urlpatterns = [
    path("memo/", views.memo_editor, name="memo_editor"),
]