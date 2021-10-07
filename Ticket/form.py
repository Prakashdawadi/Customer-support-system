from django import forms
from .models import Ticket, ticketAssign,ticketConversation

class ticketForm(forms.ModelForm):
    subject = forms.CharField(
       label= 'Subject', min_length=3,max_length=20, widget=forms.TextInput(
            attrs={
                'class':'form form-control',
                 'placeholder':'enter the ticket name'
            }
        )
    )
    description = forms.CharField(
       label= 'Description', required=False, min_length=3,max_length=100, widget=forms.Textarea(
            attrs={
                'class':'form form-control',
                 'placeholder':'enter the description',
                 'row':10,
                 'col':5,
            }
        )
    )
    image = forms.FileField(required=False)
    #category = forms.CharField(label="choose the category",widget=forms.Select(attrs={'class':'form form-control'}))

    class Meta:
        model = Ticket
        fields = ['subject','description','category','image']
