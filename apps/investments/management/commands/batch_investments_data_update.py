import pandas

from django.core.management.base import BaseCommand

from apps.investments.models import AssetGroupInfo, UserAssetInfo
from apps.users.models import UserInfo


class Command(BaseCommand):
    help = '매일 변경되는 데이터셋을 읽어 DB데이터를 업데이트 합니다.'
    '''
    매일 업데이트되는 데이터를 API에서 사용가능하도록 정제하여 Django의 manage.py의 command를 이용하여 Batch 가능하도록 구현
    명령어 : python manage.py batch_investments_data_update
    '''
    def handle(self, *args, **options):        
        df  = pandas.read_excel('data/account_asset_info_set.xlsx')
        df1 = pandas.read_excel('data/asset_group_info_set.xlsx')

        group_info_list = [{
            "group_name"    : row["종목명"],
            "isin"          : row["ISIN"],
            "group_category": row["자산그룹"]
            } for i, row in df1.iterrows()] 

        for group_info in group_info_list:
            AssetGroupInfo.objects.update_or_create(
                group_name     = group_info["group_name"],
                isin           = group_info["isin"],
                group_category = group_info["group_category"]
                )

        asset_info_list= [{
            "account_number": row["계좌번호"],
            "asset_group"   : row["ISIN"],
            "current_price" : row["현재가"],
            "count"         : row["보유수량"]
            }for i, row in df.iterrows()]

        for asset_info in asset_info_list:
            user_info        = UserInfo.objects.get(account_number = asset_info["account_number"])
            asset_group_info = AssetGroupInfo.objects.get(isin = asset_info["asset_group"])
            UserAssetInfo.objects.update_or_create(
                user_id          = user_info.id,
                asset_group_id   = asset_group_info.id,
                current_price = asset_info["current_price"],
                count         = asset_info["count"] 
            )
        return "DATA_UPDATE_SUCCESS"