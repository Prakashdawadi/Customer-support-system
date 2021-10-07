from django import forms
from .models import Category
status =(
    ('active','active'),
    ('inactive','inactive')
)

class categoryForm(forms.ModelForm):
    category = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'enter your category name','class':'form-control'}))
    status  = forms.CharField(label='status', widget=forms.Select(choices=status, attrs={'class':'form-control'}))

    class Meta:
        model = Category
        fields = ['category','status']

    # def __init__(self, *args, **kwargs):
    #     super(categoryForm, self).__init__(*args, **kwargs)
    #     self.fields['category'].widget.attrs['autocomplete'] = 'off'



