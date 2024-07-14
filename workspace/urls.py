from django.urls import path
from . import views


urlpatterns = [
    path('', views.workspace, name='workspace'),
    path('news/', views.workspace),
    path('news/<int:id>/update/', views.update_news, name='update_news'),
    path('news/<int:id>/delete/', views.delete_news, name='delete_news'),
    path('news/create/', views.create_news, name='create_news'),
]