from rest_framework import serializers

from apps.investments.models import AccountBasicInfo, AccountInfo, UserAssetInfo
from apps.users.models import User


class AccountBasicInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountBasicInfo
        fields = ['in_principal']


class AccountInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountInfo
        fields = "__all__"


class UserInvestmentSerializer(serializers.ModelSerializer):
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
    accountbasicinfo_set = AccountBasicInfoSerializer(many=True)
    total_profits = serializers.SerializerMethodField()
    investment_earnings = serializers.SerializerMethodField()

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
        # 총 수익금
        user_assets  = UserAssetInfo.objects.filter(user_id = obj.id)
        asset_list   = [(user_asset.count) * (user_asset.current_price) for user_asset in user_assets]
        total_asset  = sum(asset_list)
        in_principal = AccountBasicInfo.objects.get(user_id = obj.id).in_principal
        result       = total_asset - in_principal
        return int(result)

    def get_investment_earnings(self, obj):
        # 총 수익률
        # 결과물이 소수점 으로 나올경우 소수점 2자리 까지 표기
        user_assets   = UserAssetInfo.objects.filter(user_id = obj.id)
        asset_list    = [(user_asset.count) * (user_asset.current_price) for user_asset in user_assets]
        total_asset   = sum(asset_list)
        in_principal  = AccountBasicInfo.objects.get(user_id = obj.id).in_principal
        total_profits = total_asset - in_principal
        result        = total_profits / (in_principal)*100
        return round(result, 2)