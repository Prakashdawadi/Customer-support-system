from django import forms
from .models import User
from django.utils import timezone

class CustomerProfile(forms.ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form form-control',
            'placeholder': 'enter your full name',
            'max': 20,
            'min': 5,

        }))
    phone_no = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form form-control',
            'placeholder': 'enter your mobile number',
            'max': 10,

        }))
    image = forms.ImageField(required=False)

    address = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form form-control',
            'placeholder': 'enter your  address',
            'max': 50,
            'min': 5,
        }))

    class Meta:
       model = User
       fields = ['name', 'phone_no', 'image', 'address']

class changePasswordForm(forms.ModelForm):

    password =forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form form-control',
        'min':5,
        'max':20,
        'placeholder':'enter the password'
    }))
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form form-control',
        'placeholder': 'enter the old password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form form-control',
        'placeholder': 'enter your password again'

    }))

    class Meta:
        model = User
        fields = ['old_password','password','confirm_password']
    # sanitize your change your  password input  section


    def clean(self):
        cleaned_data = super(changePasswordForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "Sorry! password does not match ")

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'enter your email',
        }))

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'form form-control',
                'placeholder':'enter your password'
            }
        )
    )



class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class':'form-control',
            'placeholder':'enter your email',
        }))
    name  = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form form-control',
            'placeholder':'enter your full name',
            'max':20,
            'min':5,
        }))
    phone_no = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form form-control',
            'placeholder': 'enter your mobile number',
            'max': 20,
            'min': 5,
        }))
    address = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form form-control',
            'placeholder': 'enter your  address',
            'max': 50,
            'min': 5,
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form form-control',
            'placeholder': 'enter your  password',
            'max': 12,
            'min': 5,
        }))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form form-control',
            'placeholder': 'enter your  password again',
            'max': 12,
            'min': 5,
        }))
    class Meta:
        model = User
        fields = ['name','email','phone_no','address','password']
        
        #sanitize the user input section
    def clean(self):
        cleaned_data = super(UserCreationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password :
            self.add_error('confirm_password',"Sorry! password does not match ")

        return cleaned_data

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=commit)
        user.last_login = timezone.now()
        if commit:
            user.save()
        return  user


