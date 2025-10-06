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

class HouseSuggestionForm(forms.Form):
    PRIORITY_CHOICES = [
        ('A', '誰かに継承したい / 住みたい'),
        ('B', '資産を現金化したい / 手放したい'),
        ('C', 'すぐには決められない / とりあえず貸したい'),
    ]
    priority = forms.ChoiceField(label='最優先の意向', choices=PRIORITY_CHOICES, widget=forms.RadioSelect, required=True)

    # ステップ2分岐はJavaScriptや別画面で分けてもOKですが、今回は同一フォームで実装
    STEP2A_CHOICES = [
        ('A-1', '恒久的に住む / 賃貸に出す'),
        ('A-2', '時々利用する (別荘、親族の集まりなど)'),
        ('A-3', '今は利用しないが、将来残したい'),
    ]
    step2a = forms.ChoiceField(label='利用頻度', choices=STEP2A_CHOICES, widget=forms.RadioSelect, required=False)

    STEP2B_CHOICES = [
        ('B-1', '築浅/状態良好'),
        ('B-2', '築古/状態不良'),
        ('B-3', '土地の面積が広い'),
    ]
    step2b = forms.ChoiceField(label='建物の状態', choices=STEP2B_CHOICES, widget=forms.RadioSelect, required=False)

    STEP2C_CHOICES = [
        ('C-1', '収益を得たい'),
        ('C-2', '管理コストを下げたい'),
    ]
    step2c = forms.ChoiceField(label='一時運用で重視すること', choices=STEP2C_CHOICES, widget=forms.RadioSelect, required=False)