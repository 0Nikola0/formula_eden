from django.contrib import admin
from .models import Poraka


class PorakaAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)
    list_display = ('sender', 'timestamp')


admin.site.register(Poraka, PorakaAdmin)
