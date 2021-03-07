from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *


class TitleAdmin(ModelAdmin):
    pass


class CategoryAdmin(ModelAdmin):
    pass


class StudioAdmin(ModelAdmin):
    pass


class SeasonAdmin(ModelAdmin):
    pass


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Studio, StudioAdmin)
admin.site.register(Season, SeasonAdmin)
