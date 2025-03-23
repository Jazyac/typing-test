from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/<str:game_type>/', views.game, name='game'),
    path('get_text/<str:game_type>/', views.get_text, name='get_text'),
    path('save_result/', views.save_result, name='save_result'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
] 