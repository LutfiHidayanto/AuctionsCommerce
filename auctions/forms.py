from django.forms import ModelForm
from .models import *

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title',
                  'description',
                  'image',
                  'price',
                  'category',
                  'duration' 
                  ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['duration'].widget.attrs['placeholder'] = 'Hours'
            for visible in self.fields:
                visible.widget.attrs['class'] = 'form-control'
