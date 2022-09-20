from django.urls import path

from api.v1.investments.views import InvestmentDetailView, InvestmentHomeView

urlpatterns = [
    path("home/", InvestmentHomeView.as_view()),
    path("detail/", InvestmentDetailView.as_view()),
]
