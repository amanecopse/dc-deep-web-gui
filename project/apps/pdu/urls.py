from .views import PduView
from django.urls import path

app_name = 'pdu'

urlpatterns = [
    path('', PduView.as_view(), name='index'),
]
