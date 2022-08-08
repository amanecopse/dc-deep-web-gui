from .views import IndexView
from django.contrib.auth import views as auth_views
from django.urls import path

app_name = 'app'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
