from django.contrib import admin

from .models import Site


class AdminSite(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Site, AdminSite)
