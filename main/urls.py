from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.main, name='home'),
    path('help', views.help, name='help'),
    path('user', views.user_manage, name='user'),
    path('toggle_staff_status/<int:user_id>/', views.toggle_staff_status, name='toggle_staff_status'),
    path('register', views.register_request, name='register'),
    path('login', views.login_request, name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='main/logout.html'), name='logout'),
    path('search/', views.search_view_users, name='search_results_users'),
]
