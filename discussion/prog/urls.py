from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),

    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.profile, name='profile'),

    path('create-room', views.create_room, name='create-room'),
    path('update-room/<str:pk>/', views.update_room, name='update-room'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete-room'),
    path('delete-message/<str:pk>/', views.delete_message, name='delete-message'),

    path('test', views.test)
    
]