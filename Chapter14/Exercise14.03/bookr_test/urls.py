from django.urls import path
from . import views

urlpatterns = [
   path('test/greeting', views.greeting_view, name='greeting_view')
]
