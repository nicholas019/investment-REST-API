import hashlib
from rest_framework import generics
from rest_framework.views import APIView, Response
from api.v1.investments.serializers import  AccountBasicInfoSerializer, HoldingsListSerializer, TradeInfoSerializer, UserInvestmentDetailSerializer, UserInvestmentSerializer
from apps.investments.models import AccountBasicInfo, TradeInfo, UserAssetInfo

from apps.users.models import User


class InvestmentHomeView(generics.ListAPIView):
    '''
    투자화면 API
    토큰을 통해 유저정보를 받아 고객이름, 계좌명, 증권사. 계좌번호, 계좌 총 자산 총 5가지 항목 반환
    '''
    serializer_class = UserInvestmentSerializer

    def get_queryset(self):
        user     = self.request.user
        queryset = User.objects.filter(id = user.id)

        return queryset


class InvestmentDetailView(InvestmentHomeView):
    '''
    투자 상세 화면 API구현
    고객이름, 계좌명, 증권사, 계좌번호, 계좌 총 자산, 투자 원금, 총 수익금, 수익률 8개 데이터 반환
    '''
    serializer_class = UserInvestmentDetailSerializer


class HoldingsView(generics.ListAPIView):    
    '''
    보유종목 화면 API 구현
    고객이름, 보유 종목명, 보유 종목의 자산그룹, 보유 종목의 평가 금액, 보유 종목 ISIN 5개 데이터 반환

    '''
    serializer_class = HoldingsListSerializer

    def get_queryset(self):
        user     = self.request.user
        queryset = UserAssetInfo.objects.filter(user_id = user.id)
        return queryset


class CreateTradeInfo(generics.CreateAPIView):
    '''
    입금거래 정보 저장 API
    정상적으로 입금시 id 반환
    '''
    queryset         = TradeInfo.objects.all()
    serializer_class = TradeInfoSerializer


class UpdateUserAssetView(APIView):
    '''
    등록한 거래정보 검증 후 실제 고객의 자산 업데이트 API
    계좌번호 + 고객이름 + 투자금액 을 sha512로 만든 해시값과 기존 입금거래정보 의 계좌번호 + 고객이름 + 투자금액을 
    sha512로 해시한값과 비교후에 맞다면 투자원금에 투자금액을 더하는 기능 구현
    투자금액을 더한뒤 기존에 있던 입금거래정보는 삭제
    '''
    def post(self, request):
        data= self.request.data
        id        = data["id"]
        signature = data["signature"]

        trade_info  = TradeInfo.objects.get(id = id)
        data        = str(trade_info.account_number) + str(trade_info.user_name) + str(int(trade_info.transfer_amount))
        hash_data   = hashlib.sha512()
        hash_data.update(data.encode('utf-8'))
        hash_result = hash_data.hexdigest()
        
        if signature == hash_result:
            AccountBasicInfo.objects.filter(user_id = id).update(in_principal = trade_info.transfer_amount)
            trade_info.delete()
            return Response({"status":'True'})
        return Response({"status":"False"})
