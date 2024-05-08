from django.urls import path
from . import views

urlpatterns = [
    path('', views.users_list, name='users_list'),
    path('create/', views.save_user, name='save_user'),
    path('update/<int:pk>/', views.update_user, name='update_user'),
    path('delete/<int:pk>/', views.delete_user, name='delete_user'),
    path('login/', views.user_login, name='login'),
]