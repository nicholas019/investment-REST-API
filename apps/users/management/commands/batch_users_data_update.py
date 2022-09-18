import collections, pandas

from django.core.management.base import BaseCommand

from apps.users.models import AccountBasicInfo, UserInfo


class Command(BaseCommand):
    help = '매일 변경되는 데이터셋을 읽어 DB데이터를 업데이트 합니다.'
    '''
    매일 업데이트되는 데이터를 API에서 사용가능하도록 정제하여 Django의 manage.py의 command를 이용하여 Batch 가능하도록 구현
    명령어 : python manage.py batch_users_data_update
    '''
    def handle(self, *args, **options):
        df  = pandas.read_excel('data/account_asset_info_set.xlsx')
        df1 = pandas.read_excel('data/account_basic_info_set.xlsx')

        user_info_list= [{
            "username"      : row["고객이름"],
            "account_number": row["계좌번호"],
            "account_name"  : row["계좌명"],
            "stock_firm"    : row["증권사"]
            }for i, row in df.iterrows()]

        user_info_list1=list(map(dict, collections.OrderedDict.fromkeys(tuple(sorted(user_info.items())
                ) for user_info in user_info_list)))

        for user in user_info_list1:
            UserInfo.objects.update_or_create(
                username       = user["username"],
                account_number = user["account_number"],
                account_name   = user["account_name"],
                stock_firm     = user["stock_firm"]
                )

        basic_info_list= [{
            "account_number": row["계좌번호"],
            "in_principal"  : row["투자원금"]
            }for i, row in df1.iterrows()]

        for basic in basic_info_list:
            user_info = UserInfo.objects.get(account_number = basic["account_number"])

            AccountBasicInfo.objects.update_or_create(
                user_id      = user_info.id,
                in_principal = int(basic["in_principal"])
            )

        return "DATE_UPDATE_SUCCESS"