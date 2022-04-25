
# forms.py
from django import forms
from .models import *
  
class ImageForm(forms.ModelForm):
  
    class Meta:
        model = Image_recognize
        fields = ['name', 'Image_recognize_main']