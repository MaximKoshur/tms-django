from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('articles/like', views.like, name='like'),
    path('articles/<int:article_id>/', views.articles_id, name='articles_id'),
    path('articles/', views.index, name='articles'),
    path('authors/<int:author_id>/', views.author_detail, name='author_detail'),

]

