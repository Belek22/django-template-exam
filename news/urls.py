from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('news/<int:pk>/', views.detail_news, name='detail_news'), 
    path('category/<int:id>/', views.news_by_category, name='news_by_category'),
    path('news/category/<int:id>/', views.news_by_category, name='news_by_category'),
] 