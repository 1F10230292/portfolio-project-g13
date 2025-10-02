from django import forms
from .models import Inheritance

class HouseDetailForm(forms.ModelForm):
    class Meta:
        model = Inheritance
        fields = ['address', 'built_year', 'size', 'has_house']
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': '例：東京都新宿区○○町1-2-3'}),
            'built_year': forms.NumberInput(attrs={'placeholder': '例：2005'}),
            'size': forms.NumberInput(attrs={'placeholder': '例：120'}),
            'has_house': forms.RadioSelect(choices=[(True,'あり'),(False,'なし')])
        }
