from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path("", views.top, name="top"),  # トップページ
    path("login/", views.login_view, name="login"),  # ログインページ
    path("register/", views.register, name="register"),
    path("inheritance/", views.inheritance_input, name="inheritance_input"),  # 相続情報の入力
    path('transfer/<int:pk>/', views.transfer_password_view, name='transfer_password'),
    path('heir/login/', views.heir_login, name='heir_login'),
    path("house/<int:pk>/", views.house_detail, name="house_detail"),
    path("house/<int:pk>/edit/", views.house_detail_input, name="house_detail_input"),
    path("house/<int:pk>/suggestion/", views.house_suggestion, name="house_suggestion"),
    path("house/<int:pk>/sell/", views.house_sell, name="house_sell"),
path("house/<int:pk>/rent/", views.house_rent, name="house_rent"),
path("house/<int:pk>/reform/", views.house_reform, name="house_reform"),
path("house/<int:pk>/hold/", views.house_hold, name="house_hold"),

]
