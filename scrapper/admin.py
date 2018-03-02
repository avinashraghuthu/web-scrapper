from django.contrib import admin
from models import *
# Register your models here.


class ScrapperInformationAdmin(admin.ModelAdmin):
	list_per_page = 100
	search_fields = ['web_url', ]

admin.site.register(ScrapperInformation, ScrapperInformationAdmin)