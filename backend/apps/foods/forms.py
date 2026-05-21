from django import forms
from .models import Food

class FoodForm(forms.ModelForm):
    quantity = forms.ChoiceField(
        label="数量",
        choices=[(i, i) for i in range(1, 11)]
    )

    class Meta:
        model = Food
        fields = [
            "name",
            "image",
            "quantity",
            "expiration_date",
            "no_expiration_date",
            "category",
            "custom_category",
        ]
        widgets = {
            "expiration_date": forms.DateInput(attrs={"type": "date"}),
        } 
