from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class MessageboardConfig(AppConfig):
    name = 'messageboard'

class MessageboardAdminConfig(AdminConfig):
    default_site = 'admin.Comment8orAdminSite'
