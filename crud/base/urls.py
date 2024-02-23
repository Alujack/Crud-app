from django.urls import path
from base import views
urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.create, name='signup'),
    path('read/', views.read, name="read"),
    path('update/<str:pk>/', views.update, name="update"),
    path('delete/<str:pk>/', views.delete, name="delete"),
    path('login/', views.login_req, name='login'),
    path('logout/', views.logoutUser, name='logout'),


]
