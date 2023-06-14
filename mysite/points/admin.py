from django.contrib import admin
from .models import *

@admin.action(description="Рассоединить данные точки(Только 2 точки)")
def disconnect(self, request, queryset):
    if (len(queryset) == 2):
        queryset[0].disconnect(queryset[1])

@admin.action(description="Cоединить данные точки(Только 2 точки)")
def connect(self, request, queryset):
    if (len(queryset) == 2):
        queryset[0].connect(queryset[1])

class PointAdminSite(admin.ModelAdmin):
    model = Point

    list_display = ("institue", "type", "floor", "relativeX", "relativeY")
    ordering = ["id"]

    actions = [disconnect, connect]

admin.site.register(Institue)
admin.site.register(ClassRoom)
admin.site.register(Point, PointAdminSite)