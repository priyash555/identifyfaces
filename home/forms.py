from .models import TestImages
from django import forms

class TestImageform(forms.ModelForm):
    
    class Meta:
        model =  TestImages
        fields = ['GroupImage',
                'PersonImage'
                ]

