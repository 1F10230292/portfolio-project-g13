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

]
