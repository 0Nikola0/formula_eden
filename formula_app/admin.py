from django.contrib import admin
from .models import Tim, Vozac, Sesija, Trka, Vest, TrkaSesija


class TimAdmin(admin.ModelAdmin):
    list_display = ('ime',)

    
class VozacAdmin(admin.ModelAdmin):
    list_display = ('ime', 'prezime', 'tim')

    
class SesijaAdmin(admin.ModelAdmin):
    readonly_fields = ('session_id',)
    list_display = ('session_id', 'ime', 'trka_ime', 'datum')

    
class TrkaAdmin(admin.ModelAdmin):
    readonly_fields = ('race_id',)
    list_display = ('ime', 'pocetok', 'status')

    
class VestAdmin(admin.ModelAdmin):
    readonly_fields = ('custom_id',)
    list_display = ('naslov', 'skrejp_datum')


class TrkaSesijaAdmin(admin.ModelAdmin):
    list_display = ('trka', 'sesija')


admin.site.register(Tim, TimAdmin)
admin.site.register(Vozac, VozacAdmin)
admin.site.register(Sesija, SesijaAdmin)
admin.site.register(Trka, TrkaAdmin)
admin.site.register(Vest, VestAdmin)
admin.site.register(TrkaSesija, TrkaSesijaAdmin)
