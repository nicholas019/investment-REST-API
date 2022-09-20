from rest_framework import serializers
from api.v1.users.serializers import UserSerializer

from apps.users.models import User
from apps.investments.models import AccountBasicInfo, AccountInfo, AssetGroupInfo, UserAssetInfo


class AssetGroupSerialzer(serializers.ModelSerializer):
    class Meta:
        model  = AssetGroupInfo
        fields = "__all__"


class AccountBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AccountBasicInfo
        fields = ['in_principal']


class AccountInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AccountInfo
        fields = "__all__"


class UserInvestmentSerializer(serializers.ModelSerializer):
    '''
    투자화면 시리얼라이저 API
    '''
    account     = AccountInfoSerializer()
    total_asset = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', "username", "account", "total_asset"]
        

    def get_total_asset(self, obj):
        '''
        DB에 없는 '계좌 총 자산'을 연산해 serializer에 MethodField를 활용해 추가
        '''
        user_assets = UserAssetInfo.objects.filter(user_id = obj.id)
        result      = [(user_asset.count) * (user_asset.current_price) for user_asset in user_assets]
        result      = int(sum(result))
        
        return result


class UserInvestmentDetailSerializer(UserInvestmentSerializer):
    '''
    투자 상세화면 API 시리얼라이저
    '''
    accountbasicinfo_set = AccountBasicInfoSerializer(many=True)
    total_profits        = serializers.SerializerMethodField()
    investment_earnings  = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 
            "username", 
            "account", 
            "total_asset", 
            "accountbasicinfo_set", 
            "total_profits",
            "investment_earnings"
            ]
    
    def get_total_profits(self, obj):
        '''총 수익금'''
        user_assets  = UserAssetInfo.objects.filter(user_id = obj.id)
        asset_list   = [(user_asset.count) * (user_asset.current_price) for user_asset in user_assets]
        total_asset  = sum(asset_list)
        in_principal = AccountBasicInfo.objects.get(user_id = obj.id).in_principal
        result       = total_asset - in_principal

        return int(result)

    def get_investment_earnings(self, obj):
        '''
        총 수익률
        결과물이 소수점 으로 나올경우 소수점 2자리 까지 표기
        '''
        user_assets   = UserAssetInfo.objects.filter(user_id = obj.id)
        asset_list    = [(user_asset.count) * (user_asset.current_price) for user_asset in user_assets]
        total_asset   = sum(asset_list)
        in_principal  = AccountBasicInfo.objects.get(user_id = obj.id).in_principal
        total_profits = total_asset - in_principal
        result        = total_profits / (in_principal)*100

        return round(result, 2)


class HoldingsListSerializer(serializers.ModelSerializer):
    '''
    보유종목 회면 API 시리얼라이저
    '''
    user                     = UserSerializer()
    asset_group              = AssetGroupSerialzer()
    holdings_evaluated_price = serializers.SerializerMethodField()
    class Meta:
        model = UserAssetInfo
        fields = [
            "id",
            "user",
            "asset_group",
            "holdings_evaluated_price"
            ]

    def get_holdings_evaluated_price(self, obj):
        # 보유종목의 평가금액 
        current_price = obj.current_price
        count         = obj.count
        result        = current_price * count

        return int(result)