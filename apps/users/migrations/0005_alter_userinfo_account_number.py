# Generated by Django 4.1 on 2022-09-18 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='account_number',
            field=models.BigIntegerField(verbose_name='계좌번호'),
        ),
    ]