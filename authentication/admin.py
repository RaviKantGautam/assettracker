from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

# Customize the admin site
admin.site.site_header = _('Asset Tracker Administration')
admin.site.site_title = _('Asset Tracker Administration')
admin.site.index_title = _('Asset Tracker')

# Register your models here.
admin.site.register(User)
admin.site.unregister(Group)