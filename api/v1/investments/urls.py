from django.urls import path

from api.v1.investments.views import InvestmentHomeView

urlpatterns = [
    path("home/", InvestmentHomeView.as_view()),
]
