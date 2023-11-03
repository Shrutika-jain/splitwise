from django.urls import path
from rest_framework import routers
from django.urls.conf import include
from .views import SplitBillApiView, UserPassbookView

router = routers.DefaultRouter()

app_name = 'api'
urlpatterns = [
    path('', include(router.urls), name="api"),
    path('/split-bill/', SplitBillApiView.as_view(), name="split_bill"),
    path('/passbook/<uuid:userid>', UserPassbookView.as_view(), name="split_bill"),
]   