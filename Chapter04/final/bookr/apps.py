from django.contrib.admin.apps import AdminConfig


class ReviewsAdminConfig(AdminConfig):
    default_site = 'admin.BookrAdminSite'
