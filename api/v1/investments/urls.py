from django.urls import path

from api.v1.investments.views import CreateTradeInfo, HoldingsView, InvestmentDetailView, InvestmentHomeView

urlpatterns = [
    path("home/", InvestmentHomeView.as_view()),
    path("detail/", InvestmentDetailView.as_view()),
    path("holdings/", HoldingsView.as_view()),
    path("trade/", CreateTradeInfo.as_view()),
]
