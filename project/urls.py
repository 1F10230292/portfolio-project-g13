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
    path('house/<int:pk>/operation/compare/', views.house_operation_compare, name='house_operation_compare'),
    path('house/<int:pk>/support/', views.house_support, name='house_support'),
    path('house/<int:pk>/measures/', views.vacant_home_measures, name='vacant_home_measures'),
    path('house/<int:pk>/estimate/', views.estimate_house_price, name='estimate_house_price'),
    path('house/<int:pk>/renovation/', views.renovation_guide, name='renovation_guide'),
    path('house/<int:pk>/reform_guide/', views.reform_guide, name='reform_guide'),
    path('house/<int:pk>/private_lodging/', views.private_lodging, name='private_lodging'),
    path("house/<int:pk>/house_reform_b1/", views.house_reform_b1, name="house_reform_b1"),
    path("house/<int:pk>/house_reform_b2/", views.house_reform_b2, name="house_reform_b2"),
    path("house/<int:pk>/house_reform_b3/", views.house_reform_b3, name="house_reform_b3"),
    path("house/<int:pk>/summary/", views.inheritance_summary, name="inheritance_summary"),
    path("house/<int:pk>/pdf/", views.inheritance_pdf, name="inheritance_pdf"),
]