from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('questions', views.QuestionViewSet)
router.register('choices', views.ChoiceViewSet)
router.register('articles', views.ArticleViewSet)
router.register('category', views.CategoryViewSet)
router.register('product', views.ProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('questions/<int:question_id>/vote', views.choice_vote),
    path('questions/<int:pk>/update/', views.QuestionViewSet.as_view({'put': 'update'}), name='question-update'),
    path('questions/<int:pk>/delete/', views.QuestionViewSet.as_view({'delete': 'destroy'}), name='question-delete'),
]
