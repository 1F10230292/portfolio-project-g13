from django.db import models
from django.contrib.auth.models import User
import random
import string

def generate_transfer_password():
    """8桁のランダム英数字パスワードを生成"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class Inheritance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inheritances", null=True, blank=True)

    # 被相続人情報
    deceased_name = models.CharField("氏名", max_length=100)
    deceased_name_kana = models.CharField("ふりがな", max_length=100, blank=True, null=True)
    deceased_birth_date = models.DateField("生年月日", blank=True, null=True)
    postal_code = models.CharField("郵便番号", max_length=10, blank=True, null=True)
    address = models.CharField("住所", max_length=255, blank=True, null=True)
    occupation = models.CharField("職業", max_length=100, blank=True, null=True)

    # 遺産手続き情報
    inheritance_settlement_date = models.DateField("遺産分割完了日YY-MM-DD", blank=True, null=True)
    tax_office = models.CharField("申告書提出先", max_length=255, blank=True, null=True)

    # 財産総額・相続人情報
    estate_value = models.DecimalField("遺産総額（円）", max_digits=15, decimal_places=0, default=0)
    heirs = models.TextField("相続人情報")
    has_house = models.BooleanField("不動産（家）の有無", default=False)

    # 不動産詳細
    house_address = models.CharField("不動産住所", max_length=255, blank=True, null=True)
    house_built_year = models.PositiveIntegerField("築年数", blank=True, null=True)
    house_size = models.DecimalField("土地/建物の面積(㎡)", max_digits=6, decimal_places=2, blank=True, null=True)

    # 財産カテゴリ（円単位）
    cash_deposit = models.DecimalField("現金・預貯金", max_digits=15, decimal_places=0, default=0)
    securities = models.DecimalField("有価証券", max_digits=15, decimal_places=0, default=0)
    household_goods = models.DecimalField("家庭用財産", max_digits=15, decimal_places=0, default=0)
    others = models.DecimalField("その他の財産", max_digits=15, decimal_places=0, default=0)
    life_insurance = models.DecimalField("生命保険・死亡退職手当", max_digits=15, decimal_places=0, default=0)
    business_assets = models.DecimalField("事業用財産", max_digits=15, decimal_places=0, default=0)
    foreign_assets = models.DecimalField("外貨（円換算）", max_digits=15, decimal_places=0, default=0)
    funeral_cost = models.DecimalField("葬儀費用", max_digits=15, decimal_places=0, default=0)
    debt = models.DecimalField("債務", max_digits=15, decimal_places=0, default=0)

    # 引継ぎパスワード
    transfer_password = models.CharField(
        "引継ぎパスワード",
        max_length=8,
        unique=True,
        default=generate_transfer_password,
        editable=False
    )

    # 作成日時
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """estate_value を財産カテゴリの合計から自動計算"""
        total_assets = (
            self.cash_deposit + self.securities + self.household_goods +
            self.others + self.life_insurance + self.business_assets +
            self.foreign_assets + self.funeral_cost - self.debt
        )
        self.estate_value = total_assets
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.deceased_name} の遺産情報"
