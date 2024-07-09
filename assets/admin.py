from django.contrib import admin
from .models import Asset, AssetType, AssetImage
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import format_html
from django.db import models


class CustomAdminFileWidget(AdminFileWidget):
    '''
    A custom widget for rendering file fields in the admin interface.

    This widget extends the default AdminFileWidget and adds additional functionality
    to display a clickable image thumbnail for the file.

    Usage:
    - Add this widget to the desired file field in the admin interface.

    Example:
    class AssetAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.ImageField: {'widget': CustomAdminFileWidget},
        }
    '''

    def render(self, name, value, attrs=None, renderer=None):
        # Generate HTML code for displaying the file and a clickable image thumbnail
        result = []
        if hasattr(value, "url"):
            result.append(
                f'''<a href="{value.url}" target="_blank">
                      <img 
                        src="{value.url}" alt="{value}" 
                        width="100" height="100"
                        style="object-fit: cover;"
                      />
                    </a>'''
            )
        result.append(super().render(name, value, attrs, renderer))
        return format_html("".join(result))


class AssetImageInline(admin.TabularInline):
    '''
    Represents an inline form for managing asset images in the admin interface.
    
    This class is used to display and manage AssetImage objects in a tabular format within the admin interface.
    It inherits from the admin.TabularInline class provided by Django.
    '''
    model = AssetImage
    extra = 1
    formfield_overrides = {
        models.ImageField: {'widget': CustomAdminFileWidget}
    }


class AssetAdmin(admin.ModelAdmin):
    # Display the name, asset type, status, and creation date of the asset in the admin interface
    inlines = [AssetImageInline]
    list_display = ('name', 'asset_type', 'status', 'created_at')


class AssetTypeAdmin(admin.ModelAdmin):
    # Display the name and creation date of the asset type in the admin interface
    list_display = ('name', 'created_at')

admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetType,AssetTypeAdmin)
