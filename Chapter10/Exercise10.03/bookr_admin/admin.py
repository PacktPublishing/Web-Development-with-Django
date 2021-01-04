from django.contrib import admin

class BookrAdmin(admin.AdminSite):
    site_header = "Bookr Administration"
    logout_template = "admin/logout.html"

