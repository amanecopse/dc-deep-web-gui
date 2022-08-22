from .views import PduView
from django.urls import path

app_name = 'pdu'

urlpatterns = [
    path('<int:rackNum>/<int:pduNum>/', PduView.as_view(), name='index'),
]
