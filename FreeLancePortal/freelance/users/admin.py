from django.contrib import admin

from .models import Profile, Rate, Value, Company, ResponseToCompany

admin.site.register(Profile)
admin.site.register(Rate)
admin.site.register(Value)
admin.site.register(Company)
admin.site.register(ResponseToCompany)