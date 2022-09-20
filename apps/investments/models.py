from django.db import models
from django.core.validators import MinValueValidator


class UserAssetInfo(models.Model): 
    user          = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="고객")
    asset_group   = models.ForeignKey("investments.AssetGroupInfo", on_delete=models.CASCADE, verbose_name="자산그룹정보")
    current_price = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name="현재가")
    count         = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="보유수량")

    class Meta:
        db_table            = "user_accset_info"
        verbose_name        = "고객자산정보"
        verbose_name_plural = verbose_name


class AssetGroupInfo(models.Model):
    group_name     = models.CharField(max_length=45, verbose_name="종목명")
    isin           = models.CharField(max_length=45, verbose_name="ISIN")
    group_category = models.CharField(max_length=45, verbose_name="자산그룹")

    class Meta:
        db_table            = "accset_group_info"
        verbose_name        = "자산그룹정보"
        verbose_name_plural = verbose_name


class AccountInfo(models.Model):
    account_number = models.BigIntegerField(verbose_name="계좌번호")
    account_name   = models.CharField(max_length=45, verbose_name="계좌명")
    stock_firm     = models.CharField(max_length=45, verbose_name="증권사")

    class Meta:
        db_table            = "account_info"
        verbose_name        = "계좌정보"
        verbose_name_plural = verbose_name


class AccountBasicInfo(models.Model):
    user         = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="고객")
    in_principal = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name="투자원금")

    class Meta:
        db_table            = "account_basic_info"
        verbose_name        = "투자정보"
        verbose_name_plural = verbose_name

