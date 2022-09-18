from django.db import models


class UserInfo(models.Model):
    username       = models.CharField(max_length=45, verbose_name="고객이름")
    account_number = models.BigIntegerField(verbose_name="계좌번호")
    account_name   = models.CharField(max_length=45, verbose_name="계좌명")
    stock_firm     = models.CharField(max_length=45, verbose_name="증권사")

    class Meta:
        db_table            = "user_info"
        verbose_name        = "고객정보"
        verbose_name_plural = verbose_name


class AccountBasicInfo(models.Model):
    user         = models.ForeignKey("users.UserInfo", on_delete=models.CASCADE, verbose_name="고객")
    in_principal = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name="투자원금")

    class Meta:
        db_table            = "account__basic_info"
        verbose_name        = "투자정보"
        verbose_name_plural = verbose_name

