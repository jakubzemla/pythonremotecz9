from django.contrib import admin

# Register your models here.
from base.models import Room
from base.models import Message

admin.site.register(Room)
admin.site.register(Message)