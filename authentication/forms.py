from typing import Any
from django import forms
from .models import *
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation



class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name','last_name')


    def __init__(self,*args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False,error_messages={"invalid":{"Image files only"}},widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields =('address_line_1','role','address_line_2','mobile','city','state','country','zipcode','profile_picture')

    def __init__(self,*args, **kwargs):
        super(UserProfileForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CustomerProfileForm(forms.ModelForm):
    # profile_picture = forms.ImageField(required=False,error_messages={"invalid":{"Image files only"}},widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ['country','role','address_line_1','address_line_2','zipcode','mobile','city','profile_picture','state']

    def __init__(self,*args, **kwargs):
        super(CustomerProfileForm,self).__init__(*args, **kwargs)
        # self.fields['country'].widget.attrs['placeholder'] = 'Enter country'
        # self.fields['address_line_1'].widget.attrs['placeholder'] = 'Enter address_line_1'
        # self.fields['address_line_2'].widget.attrs['placeholder'] = 'Enter address_line_2'
        # self.fields['city'].widget.attrs['placeholder'] = 'Enter city'
        # self.fields['state'].widget.attrs['placeholder'] = 'Enter state'
        # self.fields['zipcode'].widget.attrs['placeholder'] = 'Enter zipcode'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
