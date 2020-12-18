from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class ReviewsConfig(AppConfig):
    name = 'reviews'

class ReviewsAdminConfig(AdminConfig):
    default_site = 'admin.BookrAdminSite'

