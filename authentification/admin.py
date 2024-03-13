from django.contrib import admin

# Register your models here.
from .models import User,Friend_Link
admin.site.register(User)
admin.site.register(Friend_Link)