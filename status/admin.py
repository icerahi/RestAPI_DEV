from django.contrib import admin
from .models import Status
from .forms import StatusForm

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display =['user','__str__','image']
    form = StatusForm

