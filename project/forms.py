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

from django import forms

class HouseSuggestionForm(forms.Form):
    PRIORITY_CHOICES = [
        ('A', '誰かに継承したい / 住みたい'),
        ('B', '資産を現金化したい / 手放したい'),
        ('C', 'すぐには決められない / とりあえず貸したい'),
    ]
    priority = forms.ChoiceField(label='最優先の意向', choices=PRIORITY_CHOICES, widget=forms.RadioSelect, required=True)

class HouseUsageForm(forms.Form):
    USAGE_CHOICES = [
        ('A-1', '恒久的に住む / 賃貸に出す'),
        ('A-2', '時々利用する (別荘、親族の集まりなど)'),
        ('A-3', '今は利用しないが、将来残したい'),
    ]
    usage = forms.ChoiceField(label='物件の利用頻度', choices=USAGE_CHOICES, widget=forms.RadioSelect, required=True)