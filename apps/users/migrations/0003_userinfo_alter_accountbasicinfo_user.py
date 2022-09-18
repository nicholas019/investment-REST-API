# Generated by Django 4.1 on 2022-09-18 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_accountbasicinfo_user_account_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=45, verbose_name='고객이름')),
                ('account_number', models.IntegerField(verbose_name='계좌번호')),
                ('account_name', models.CharField(max_length=45, verbose_name='계좌명')),
                ('stock_firm', models.CharField(max_length=45, verbose_name='증권사')),
            ],
            options={
                'verbose_name': '고객정보',
                'verbose_name_plural': '고객정보',
                'db_table': 'user_info',
            },
        ),
        migrations.AlterField(
            model_name='accountbasicinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userinfo', verbose_name='고객'),
        ),
    ]