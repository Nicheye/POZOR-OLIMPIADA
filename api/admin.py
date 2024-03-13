from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Country)
admin.site.register(Publication)
admin.site.register(Like)
admin.site.register(DisLike)