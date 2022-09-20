from django.urls import path, include

urlpatterns = [
    path("user/", include("api.v1.users.urls")),
    path("invest/", include("api.v1.investments.urls")),
]
