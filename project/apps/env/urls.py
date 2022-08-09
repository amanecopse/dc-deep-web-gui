from .views import EnvView
from django.urls import path

app_name = 'env'

urlpatterns = [
    path('', EnvView.as_view(), name='index'),
]
