from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Inheritance
from .forms import InheritanceForm, HouseDetailForm, HouseSuggestionForm
import random
import string
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
import os

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
                inheritance = Inheritance.objects.filter(user=user).latest('id')
                return redirect('project:transfer_password', pk=inheritance.pk)
            else:
                return redirect('project:inheritance_input')
        else:
            messages.error(request, "ユーザー名またはパスワードが間違っています。")
    return render(request, 'project/login.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "登録が完了しました。ログインしてください。")
            return redirect('project:login')
        else:
            messages.error(request, "入力に誤りがあります。確認してください。")
    else:
        form = UserCreationForm()
    return render(request, 'project/register.html', {'form': form})


def generate_transfer_password():
    """8桁のランダム英数字パスワードを生成"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@login_required
def inheritance_input(request):
    if request.method == 'POST':
        form = InheritanceForm(request.POST)
        if form.is_valid():
            inheritance = form.save(commit=False)
            inheritance.user = request.user
            inheritance.transfer_password = generate_transfer_password()
            inheritance.save()
            messages.success(request, "登録が完了しました。引継ぎパスワードを発行します。")
            return redirect('project:transfer_password', pk=inheritance.pk)
        else:
            # バリデーションエラーをログに出力（開発用）
            print(form.errors)
            messages.error(request, "入力に誤りがあります。確認してください。")
    else:
        form = InheritanceForm()
    return render(request, 'project/inheritance_input.html', {'form': form})

@login_required
def transfer_password_view(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk)
    return render(request, 'project/transfer_password.html', {
        'inheritance': inheritance, 
        'transfer_password': inheritance.transfer_password,
        'deceased_name': inheritance.deceased_name
    })

def heir_login(request):
    """被相続人用ログインページ"""
    if request.method == 'POST':
        password = request.POST.get('transfer_password')
        try:
            inheritance = Inheritance.objects.get(transfer_password=password)
            return render(request, 'project/heir_dashboard.html', {
                'inheritance': inheritance
            })
        except Inheritance.DoesNotExist:
            return render(request, 'project/heir_login.html', {
                'error': "パスワードが間違っています。"
            })
    return render(request, 'project/heir_login.html')


@login_required
def house_detail(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk)
    return render(request, "project/house_detail.html", {"inheritance": inheritance})


@login_required
def house_detail_input(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk)
    if request.method == "POST":
        form = HouseDetailForm(request.POST, instance=inheritance)
        if form.is_valid():
            form.save()
            messages.success(request, "不動産情報を保存しました。")
            return redirect("project:house_suggestion", pk=inheritance.pk)
    else:
        form = HouseDetailForm(instance=inheritance)
    return render(request, "project/house_detail_input.html", {"form": form, "inheritance": inheritance})


@login_required
def house_suggestion(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk)
    if request.method == "POST":
        form = HouseSuggestionForm(request.POST)
        if form.is_valid():
            priority = form.cleaned_data['priority']
            if priority == 'A':
                return redirect("project:house_sell", pk=pk)
            elif priority == 'B':
                return redirect("project:house_reform", pk=pk)
            elif priority == 'C':
                return redirect("project:house_rent", pk=pk)
    else:
        form = HouseSuggestionForm()
    return render(request, "project/house_suggestion.html", {
        "form": form,
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

@login_required
def house_detail(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk)
    return render(request, "project/house_detail.html", {"inheritance": inheritance})

@login_required
def house_operation_compare(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk, user=request.user)
    return render(request, "project/house_operation_compare.html", {"inheritance": inheritance})

@login_required
def house_support(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk, user=request.user)
    return render(request, "project/house_support.html", {"inheritance": inheritance})

@login_required
def vacant_home_measures(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk, user=request.user)
    return render(request, "project/vacant_home_measures.html", {"inheritance": inheritance})

@login_required
def estimate_house_price(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk, user=request.user)
    return render(request, "project/estimate_house_price.html", {"inheritance": inheritance})

@login_required
def renovation_guide(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk, user=request.user)
    return render(request, "project/renovation_guide.html", {"inheritance": inheritance})

@login_required
def reform_guide(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk, user=request.user)
    return render(request, "project/reform_guide.html", {"inheritance": inheritance})

@login_required
def private_lodging(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk, user=request.user)
    return render(request, "project/private_lodging.html", {"inheritance": inheritance})

@login_required
def house_reform_b1(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk, user=request.user)
    return render(request, "project/house_reform_b1.html", {"inheritance": inheritance})

@login_required
def house_reform_b2(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk, user=request.user)
    return render(request, "project/house_reform_b2.html", {"inheritance": inheritance})

@login_required
def house_reform_b3(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk, user=request.user)
    return render(request, "project/house_reform_b3.html", {"inheritance": inheritance})

@login_required
def inheritance_summary(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk, user=request.user)
    return render(request, "project/inheritance_summary.html", {
        "inheritance": inheritance
    })


@login_required
def inheritance_pdf(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk, user=request.user)

    html_string = render_to_string(
        "project/inheritance_pdf.html",
        {"inheritance": inheritance}
    )

    base_url = request.build_absolute_uri("/")  # ← 超重要

    html = HTML(string=html_string, base_url=base_url)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="inheritance_summary.pdf"'
    return response