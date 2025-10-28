from django import forms
from .models import Inheritance

from django import forms
from .models import Inheritance

class DetailedInheritanceForm(forms.ModelForm):
    class Meta:
        model = Inheritance
        fields = [
            "deceased_name", "deceased_name_kana", "deceased_birth_date",
            "postal_code", "address", "occupation",
            "inheritance_settlement_date", "tax_office",
            "has_house", "heirs",
            "cash_deposit", "securities", "household_goods", "others",
            "life_insurance", "business_assets", "foreign_assets",
            "funeral_cost", "debt"
        ]
        widgets = {
            "deceased_name": forms.TextInput(attrs={"placeholder": "例：山田太郎"}),
            "deceased_name_kana": forms.TextInput(attrs={"placeholder": "例：ヤマダタロウ"}),
            "deceased_birth_date": forms.DateInput(attrs={"type": "date"}),
            "postal_code": forms.TextInput(attrs={"placeholder": "例：160-0022"}),
            "address": forms.TextInput(attrs={"placeholder": "例：東京都新宿区○○町1-2-3"}),
            "occupation": forms.TextInput(attrs={"placeholder": "例：会社員"}),
            "inheritance_settlement_date": forms.DateInput(attrs={"type": "date"}),
            "tax_office": forms.TextInput(attrs={"placeholder": "例：新宿税務署"}),
            "has_house": forms.RadioSelect(choices=[(True,'あり'),(False,'なし')]),
            "heirs": forms.Textarea(attrs={"placeholder": "例：長男 山田一郎、長女 山田花子", "rows":3}),
            "cash_deposit": forms.NumberInput(attrs={"placeholder": "例：500000"}),
            "securities": forms.NumberInput(attrs={"placeholder": "例：200000"}),
            "household_goods": forms.NumberInput(attrs={"placeholder": "例：100000"}),
            "others": forms.NumberInput(attrs={"placeholder": "例：50000"}),
            "life_insurance": forms.NumberInput(attrs={"placeholder": "例：300000"}),
            "business_assets": forms.NumberInput(attrs={"placeholder": "例：400000"}),
            "foreign_assets": forms.NumberInput(attrs={"placeholder": "例：100000"}),
            "funeral_cost": forms.NumberInput(attrs={"placeholder": "例：50000"}),
            "debt": forms.NumberInput(attrs={"placeholder": "例：-200000"}),
        }

class InheritanceForm(forms.ModelForm):
    class Meta:
        model = Inheritance
        fields = [
            'deceased_name',
            'deceased_name_kana',
            'deceased_birth_date',
            'postal_code',
            'address',
            'occupation',
            'inheritance_settlement_date',
            'tax_office',
            'has_house',
            'heirs',
            'cash_deposit',
            'securities',
            'household_goods',
            'others',
            'life_insurance',
            'business_assets',
            'foreign_assets',
            'funeral_cost',
            'debt',
        ]
        widgets = {
            'deceased_birth_date': forms.DateInput(attrs={'type': 'date'}),
        }



class HouseDetailForm(forms.ModelForm):
    class Meta:
        model = Inheritance
        fields = ['house_address', 'house_built_year', 'house_size', 'has_house']  # 修正: size → house_size
        widgets = {
            'house_address': forms.TextInput(attrs={'placeholder': '例：東京都新宿区○○町1-2-3'}),
            'house_built_year': forms.NumberInput(attrs={'placeholder': '例：2005'}),
            'house_size': forms.NumberInput(attrs={'placeholder': '例：120'}),
            'has_house': forms.RadioSelect(choices=[(True,'あり'),(False,'なし')])
        }


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