from django.db import models


class User(models.Model):
    username     = models.CharField(max_length=45, verbose_name="고객명")

    class Meta:
        db_table            = "users"
        verbose_name        = "고객"
        verbose_name_plural = verbose_name


class AccountInfo(models.Model):
    user           = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="고객")
    account_number = models.IntegerField(verbose_name="계좌번호")
    account_name   = models.CharField(max_length=45, verbose_name="계좌명")
    stock_firm     = models.CharField(max_length=45, verbose_name="증권사")
    in_principal   = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name="투자원금")

    class Meta:
        db_table            = "account_info"
        verbose_name        = "계좌정보"
        verbose_name_plural = verbose_name
