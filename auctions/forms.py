from django.forms import ModelForm, DateTimeInput
from .models import *

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title',
                  'description',
                  'image',
                  'price',
                  'category',
                  'start_date',
                  'end_date',
                  ]
        widgets = {'start_date': DateTimeInput(attrs={'type': 'datetime-local'}), 
                   'end_date': DateTimeInput(attrs={'type': 'datetime-local'})
                    }
        labels = {'price': 'Starting Price'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class Bidform(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control m-2'
