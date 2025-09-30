from django.db import models
import random
import string

def generate_transfer_password():
    """8桁のランダムな英数字パスワードを生成"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class Inheritance(models.Model):
    deceased_name = models.CharField("被相続人の氏名", max_length=100)
    estate_value = models.DecimalField("遺産総額（万円）", max_digits=12, decimal_places=2)
    heirs = models.TextField("相続人情報")
    has_house = models.BooleanField("不動産（家）の有無", default=False)
    transfer_password = models.CharField(
        "引継ぎパスワード",
        max_length=8,
        unique=True,
        default=generate_transfer_password,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.deceased_name} ({self.transfer_password})"
