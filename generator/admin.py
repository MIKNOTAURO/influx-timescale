from django.contrib import admin

# Register your models here.
from generator.models import traffic


class test_metricsAdmin(admin.ModelAdmin):
    model=traffic
    search_fields = ('download',)
    list_display = ('download','time')

admin.site.register(traffic, test_metricsAdmin)