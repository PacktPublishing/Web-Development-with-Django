from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views, api_views

router = DefaultRouter()
router.register(r'books', api_views.BookViewSet)
router.register(r'reviews', api_views.ReviewViewSet)

urlpatterns = [
    path('api/login', api_views.Login.as_view(), name='login'),
    path('api/', include((router.urls, 'api'))),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:book_pk>/reviews/new/', views.review_edit, name='review_create'),
    path('books/<int:book_pk>/reviews/<int:review_pk>/', views.review_edit, name='review_edit'),
    path('books/<int:pk>/media/', views.book_media, name='book_media'),
    path('publishers/<int:pk>/', views.publisher_edit, name='publisher_detail'),
    path('publishers/new/', views.publisher_edit, name='publisher_create')
]
