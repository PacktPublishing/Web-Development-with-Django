from django.urls import path
from . import views, api_views

urlpatterns = [
    path('api/first_api_view/', api_views.first_api_view),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:book_pk>/reviews/new/', views.review_edit, name='review_create'),
    path('books/<int:book_pk>/reviews/<int:review_pk>/', views.review_edit, name='review_edit'),
    path('books/<int:pk>/media/', views.book_media, name='book_media'),
    path('publishers/<int:pk>/', views.publisher_edit, name='publisher_detail'),
    path('publishers/new/', views.publisher_edit, name='publisher_create')
]
