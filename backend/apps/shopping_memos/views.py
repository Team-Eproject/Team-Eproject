from django.shortcuts import render


def memo_editor(request):
    return render(request, "shopping_memos/memo_edit.html")