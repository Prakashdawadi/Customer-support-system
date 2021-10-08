from django import forms
from .models import Ticket, ticketAssign,ticketConversation
from Category.models import Category, status


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
                'class': 'form form-control',


            }
        )
    )
    image = forms.FileField(required=False)
    category = forms.ModelChoiceField(
        label="choose the category", required=True,
        widget=forms.Select( attrs={'class': 'form-control'}),
        queryset=Category.objects.all().filter(status='active'))

    class Meta:
        model = Ticket
        fields = ['subject','description','image','category']
