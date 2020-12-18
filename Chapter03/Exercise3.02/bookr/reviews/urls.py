from django.urls import path
from . import views

urlpatterns = [
    path('', views.simple_template_view, name='template_view'),
]
