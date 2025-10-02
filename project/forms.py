from django import forms
from .models import Inheritance

class HouseDetailForm(forms.ModelForm):
    class Meta:
        model = Inheritance
        fields = ['house_address', 'house_built_year']  # 追加したフィールド
        widgets = {
            'house_address': forms.TextInput(attrs={'placeholder': '住所を入力'}),
            'house_built_year': forms.NumberInput(attrs={'placeholder': '築年数'}),
        }
