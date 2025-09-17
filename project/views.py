from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"{username} さん、ログインしました。")
            return redirect('project:home')  # ログイン後の遷移先に変更
        else:
            messages.error(request, "ユーザー名またはパスワードが間違っています。")
    
    return render(request, 'project/login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # ユーザー作成
            messages.success(request, "登録が完了しました。ログインしてください。")
            return redirect('project:login')  # ログインページへリダイレクト
        else:
            messages.error(request, "入力に誤りがあります。確認してください。")
    else:
        form = UserCreationForm()  # GET の場合は空フォーム

    return render(request, 'project/register.html', {'form': form})