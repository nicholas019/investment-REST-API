from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, uid, username, password=None):
        """
        주어진 유저아이디, 유저이름, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not uid:
            raise ValueError('Users must have an uid')

        user = self.model(
            uid      = uid,
            username = username,
            password = password
        )
        # 비밀번호는 test를 위해 hash제외
        # user.set_password(password)
        # user.save(using=self._db)
        return user

    def create_superuser(self, uid, username, password):
        """
        주어진 유저아이디, 유저이름, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다. 
        """
        user = self.create_user(
            uid      = uid,
            password = password,
            username = username,
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    uid         = models.CharField(max_length=45, verbose_name="고객아이디", unique=True)
    username    = models.CharField(max_length=45, verbose_name="고객이름")
    account     = models.OneToOneField("users.AccountInfo", on_delete=models.CASCADE, verbose_name="계좌정보", null=True)
    is_active   = models.BooleanField(verbose_name='Is active', default=True)
    date_joined = models.DateTimeField(verbose_name='가입일자', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = []

    class Meta:
        db_table            = "users"
        verbose_name        = "고객정보"
        verbose_name_plural = verbose_name
        ordering            = ('-date_joined',)


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

