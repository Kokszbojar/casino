from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('free_balance/', views.update_balance, name='free_balance'),
    path('coinflip/', views.coinflip, name='coinflip'),
]