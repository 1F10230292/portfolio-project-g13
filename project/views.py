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
import pickle
import numpy as np
from django.shortcuts import render



def top(request):
    return render(request, "project/top.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # すでに資産が登録されているか確認
            if Inheritance.objects.filter(user=user).exists():
                inheritance = Inheritance.objects.filter(user=user).latest('id')
                return redirect('project:transfer_password', pk=inheritance.pk)
            else:
                return redirect('project:inheritance_input')
        else:
            # ログイン失敗時のエラーメッセージは残しておくのが一般的です
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

@login_required
def heir_dashboard_view(request, pk):
    inheritance = get_object_or_404(Inheritance, pk=pk)
    return render(request, 'project/heir_dashboard.html', {
        'inheritance': inheritance
    })

# views.py の 101行目あたり
def heir_login(request):
    """被相続人用ログインページ"""
    if request.method == 'POST':
        password = request.POST.get('transfer_password')
        try:
            inheritance = Inheritance.objects.get(transfer_password=password)
            # render ではなく redirect に変更
            return redirect('project:heir_dashboard', pk=inheritance.pk)
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
            return redirect("project:heir_dashboard", pk=inheritance.pk)
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

# @login_required
# def estimate_house_price(request, pk):
#     inheritance = get_object_or_404(Inheritance, pk=pk, user=request.user)
#     prediction =None
#     if inheritance.has_house:
#         # テストデータを取得
#         built_year =  inheritance.house_built_year or 0# 築年数
#         size = float(inheritance.house_size or 0)# 面積　㎡
        
#         import datetime
#         current_year = datetime.date.today().year
#         age =current_year-built_year if built_year  else 0
#         input_data = np.array([[age,size]])
#         prediction= model.predict(input_data)[0][0]
#     return render(request, "project/estimate_house_price.html", {"inheritance": inheritance,"prediction":prediction})

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


# モデルと scaler を読み込み（起動時に1回）
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

def predict_view(request):
    if request.method == "POST":
        # 入力値の取得
        floor_area = float(request.POST.get("延べ床面積"))
        land_area = float(request.POST.get("土地面積"))
        age = float(request.POST.get("築年数"))
        rooms = float(request.POST.get("部屋数"))
        use_type = request.POST.get("用途地域")  # '住居系', '商業系', '工業系'
        road_type = request.POST.get("接道状況")  # '接道なし', '角地等', 'その他'
        structure = request.POST.get("建物構造")  # '木造', '非木造'
        parking = request.POST.get("駐車場あり") == "on"
        coverage = float(request.POST.get("建ぺい率"))
        capacity = float(request.POST.get("容積率"))
        land_score = float(request.POST.get("地価スコア"))
        transport_rank = float(request.POST.get("交通ランク"))

        # カテゴリ変数の one-hot（簡易）
        use_res = 1 if use_type == "住居系" else 0
        use_com = 1 if use_type == "商業系" else 0
        use_ind = 1 if use_type == "工業系" else 0

        road_none = 1 if road_type == "接道なし" else 0
        road_corner = 1 if road_type == "角地等" else 0

        non_wood = 1 if structure == "非木造" else 0
        parking_flag = 1 if parking else 0

        # 特徴量生成
        features = {
            "築年数": age,
            "用途地域_正規化_商業系": use_com,
            "面積_築年数": floor_area / (age + 1),
            "家面積_数値": floor_area,
            "用途地域_正規化_工業系": use_ind,
            "建ぺい率_正規化": coverage,
            "土地_建蔽": land_area * coverage,
            "実効建蔽率": floor_area / land_area,
            "土地_容積": land_area * capacity,
            "接道_容積": road_none * capacity,
            "実効容積率": floor_area / land_area,
            "用途地域_正規化_住居系": use_res,
            "立地_築年数": transport_rank / (age + 1),
            "土地面積_数値": land_area,
            "接道状況_正規化_角地等": road_corner,
            "1部屋あたり面積": floor_area / rooms,
            "部屋数": rooms,
            "面積_部屋数": floor_area / (rooms + 0.5),
            "延べ床面積_数値": floor_area,
            "地価スコア": land_score,
            "駐車場_あり": parking_flag,
            "容積率_正規化": capacity,
            "築年数_構造": age * non_wood,
            "接道状況_正規化_接道なし": road_none,
            "建物構造_正規化_非木造": non_wood,
            "地勢_数値": 0.0,  # 未入力なら仮で0
            "交通_ランク": transport_rank,
            "地価_交通": land_score * transport_rank,
            "LDKあり": 0.0,
            "Sあり": 0.0
        }

        feature_order = [
    "築年数",
    "用途地域_正規化_商業系",
    "面積_築年数",
    "家面積_数値",
    "用途地域_正規化_工業系",
    "建ぺい率_正規化",
    "土地_建蔽",
    "実効建蔽率",
    "土地_容積",
    "接道_容積",
    "実効容積率",
    "用途地域_正規化_住居系",
    "立地_築年数",
    "土地面積_数値",
    "接道状況_正規化_角地等",
    "1部屋あたり面積",
    "部屋数",
    "面積_部屋数",
    "延べ床面積_数値",
    "地価スコア",
    "駐車場_あり",
    "容積率_正規化",
    "築年数_構造",
    "接道状況_正規化_接道なし",
    "建物構造_正規化_非木造",
    "地勢_数値",
    "交通_ランク",
    "地価_交通",
    "LDKあり",
    "Sあり",
]

        input_array = np.array([features[k] for k in feature_order]).reshape(1, -1)
        input_scaled = scaler.transform(input_array)
        pred_log = model.predict(input_scaled)[0]
        pred_price = np.expm1(pred_log)

        return render(request, "project/predict.html", {
            "prediction": int(pred_price)
        })

    return render(request, "project/predict.html")
