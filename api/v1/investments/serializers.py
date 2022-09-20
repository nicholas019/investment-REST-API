from rest_framework import serializers
from api.v1.users.serializers import AccountInfoSerializer

from apps.investments.models import UserAssetInfo
from apps.users.models import User

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