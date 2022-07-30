from django.forms import ModelForm
from .models import note

class NoteForm(ModelForm):
    class Meta:
        model = note
        fields = ['title', 'desc', 'colour']
