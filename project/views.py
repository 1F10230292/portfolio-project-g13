from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.decorators import login_required

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
            return redirect('project:inheritance_input')  # ← ここ変更
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
    deceased_name = forms.CharField(label="被相続人の氏名", max_length=100)
    estate_value = forms.DecimalField(label="遺産総額（万円）", max_digits=12, decimal_places=2)
    heirs = forms.CharField(label="相続人情報（例：長男〇〇、長女〇〇）", widget=forms.Textarea)


@login_required
def inheritance_input(request):
    if request.method == 'POST':
        form = InheritanceForm(request.POST)
        if form.is_valid():
            # TODO: DB保存など
            messages.success(request, "相続情報を登録しました。")
            return redirect('project:inheritance_input')
    else:
        form = InheritanceForm()

    return render(request, 'project/inheritance_input.html', {'form': form})
