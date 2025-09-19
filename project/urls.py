from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path("", views.login_view, name="login"),  # ログインページ
    path("register/", views.register, name="register"),
    path('inheritance/', views.inheritance_input, name='inheritance_input'),  #相続情報の入力
]