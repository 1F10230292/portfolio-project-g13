from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.decorators import login_required
from .models import Inheritance
import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from .forms import HouseDetailForm


def top(request):
    return render(request, "project/top.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"{username} さん、ログインしました。")

            # すでに資産が登録されているか確認
            if Inheritance.objects.filter(user=user).exists():
                # 直近のInheritanceを取得してパスワード発行ページへ
                inheritance = Inheritance.objects.filter(user=user).latest('id')
                return redirect('project:transfer_password', pk=inheritance.pk)
            else:
                # 未登録なら入力ページへ
                return redirect('project:inheritance_input')
        else:
            messages.error(request, "ユーザー名またはパスワードが間違っています。")
    
    return render(request, 'project/login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # ユーザー作成
            messages.success(request, "登録が完了しました。ログインしてください。")
            return redirect('project:login')
        else:
            messages.error(request, "入力に誤りがあります。確認してください。")
    else:
        form = UserCreationForm()

    return render(request, 'project/register.html', {'form': form})


class InheritanceForm(forms.Form):
    deceased_name = forms.CharField(
        label="被相続人の氏名",
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "例：山田太郎"
        })
    )
    estate_value = forms.DecimalField(
        label="遺産総額（万円）",
        max_digits=12,
        decimal_places=2,
        widget=forms.TextInput(attrs={
            "placeholder": "例：5000"
        })
    )
    heirs = forms.CharField(
        label="相続人情報",
        widget=forms.Textarea(attrs={
            "placeholder": "例：長男 山田一郎、長女 山田花子",
            "rows": 3
        })
    )
    has_house = forms.ChoiceField(
        label="不動産（家）の有無",
        choices=[("yes", "あり"), ("no", "なし")],
        widget=forms.RadioSelect
    )

def generate_transfer_password():
    """8桁のランダム英数字パスワードを生成"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@login_required
def inheritance_input(request):
    if request.method == 'POST':
        form = InheritanceForm(request.POST)
        if form.is_valid():
            transfer_password = generate_transfer_password()
            inheritance = Inheritance.objects.create(
                user=request.user,
                deceased_name=form.cleaned_data['deceased_name'],
                estate_value=form.cleaned_data['estate_value'],
                heirs=form.cleaned_data['heirs'],
                has_house=(form.cleaned_data['has_house'] == "yes"),
                transfer_password=transfer_password
            )
            return redirect('project:transfer_password', pk=inheritance.pk)
    else:
        form = InheritanceForm()
    return render(request, 'project/inheritance_input.html', {'form': form})


@login_required
def transfer_password_view(request, pk):
    inheritance = Inheritance.objects.get(pk=pk)
    return render(request, 'project/transfer_password.html', {
        'transfer_password': inheritance.transfer_password,
        'deceased_name': inheritance.deceased_name
    })

def heir_login(request):
    """被相続人用ログインページ"""
    if request.method == 'POST':
        password = request.POST.get('transfer_password')

        try:
            inheritance = Inheritance.objects.get(transfer_password=password)
            # ログイン成功 → 遺産情報表示ページへ
            return render(request, 'project/heir_dashboard.html', {
                'inheritance': inheritance
            })
        except Inheritance.DoesNotExist:
            # パスワード不一致
            return render(request, 'project/heir_login.html', {
                'error': "パスワードが間違っています。"
            })

    return render(request, 'project/heir_login.html')

def house_detail(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk)
    return render(request, "project/house_detail.html", {
        "inheritance": inheritance
    })

@login_required
def house_detail_input(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk)

    if request.method == "POST":
        form = HouseDetailForm(request.POST, instance=inheritance)
        if form.is_valid():
            form.save()
            messages.success(request, "不動産情報を保存しました。")
            # 保存後に提案フローへ誘導
            return redirect("project:house_suggestion", pk=inheritance.pk)
    else:
        form = HouseDetailForm(instance=inheritance)

    return render(request, "project/house_detail_input.html", {"form": form, "inheritance": inheritance})

@login_required
def house_suggestion(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk)

    # シンプルに選択肢を表示（後で分岐アンケート化できる）
    return render(request, "project/house_suggestion.html", {
        "inheritance": inheritance
    })

@login_required
def house_sell(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk)
    return render(request, "project/house_sell.html", {"inheritance": inheritance})

@login_required
def house_rent(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk)
    return render(request, "project/house_rent.html", {"inheritance": inheritance})

@login_required
def house_reform(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk)
    return render(request, "project/house_reform.html", {"inheritance": inheritance})

@login_required
def house_hold(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk)
    return render(request, "project/house_hold.html", {"inheritance": inheritance})
