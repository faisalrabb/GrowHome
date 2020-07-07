from django.contrib import admin
from account.models import Entrepreneur, Contributor, Key, Country
# Register your models here.
admin.site.register(Entrepreneur)
admin.site.register(Contributor)
admin.site.register(Key)
admin.site.register(Country)