from django.contrib import admin
from .models import note
# Register your models here.

class notesDate(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(note, notesDate)
