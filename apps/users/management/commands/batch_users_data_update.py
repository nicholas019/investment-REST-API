import collections, pandas

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.investments.models import AccountBasicInfo

from apps.users.models import AccountInfo, User


class Command(BaseCommand):
    help = '매일 변경되는 데이터셋을 읽어 DB데이터를 업데이트 합니다.'
    '''
    매일 업데이트되는 데이터를 API에서 사용가능하도록 정제하여 Django의 manage.py의 command를 이용하여 Batch 가능하도록 구현
    명령어 : python manage.py batch_users_data_update
    '''
    @transaction.atomic
    def handle(self, *args, **options):
        df  = pandas.read_excel('data/account_asset_info_set.xlsx')
        df1 = pandas.read_excel('data/account_basic_info_set1.xlsx')

        user_info_list= [{
            "username"      : row["고객이름"],
            "account_number": row["계좌번호"],
            "account_name"  : row["계좌명"],
            "stock_firm"    : row["증권사"]
            }for i, row in df.iterrows()]

        user_info_list1=list(map(dict, collections.OrderedDict.fromkeys(tuple(sorted(user_info.items())
                ) for user_info in user_info_list)))

        for user in user_info_list1:
            account = AccountInfo.objects.update_or_create(
                account_number = user["account_number"],
                account_name   = user["account_name"],
                stock_firm     = user["stock_firm"]
            )
            User.objects.update_or_create(
                username = user["username"],
                account_id = account[0].id
                )
            
        basic_info_list= [{
            "account_number": row["계좌번호"],
            "in_principal"  : row["투자원금"]
            }for i, row in df1.iterrows()]

        for basic in basic_info_list:
            user = User.objects.get(account__account_number = basic["account_number"])
            
            obj, created = AccountBasicInfo.objects.get_or_create(
                uid          = user.id,
                in_principal = int(basic["in_principal"])
                )
            if not created:
                # 새로 변경된 투자원금이 저장되고 이전에 저장되어있던 투자원금 데이터는 삭제
                result = AccountBasicInfo.objects.filter(user_id = user.id).first()
                result.delete()
            else:
                pass

        return "DATE_UPDATE_SUCCESS"