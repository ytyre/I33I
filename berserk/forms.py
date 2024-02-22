from django import forms
from django.forms import ModelForm 
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserCreationForm
from berserk.validators.validator_name import Validator_name
from berserk.validators.validator_password import Validator_passwod

from .models import br, Comment, ExtraInformation, AdvUser, SerarchRecord, ImagesAdmin


class formI(ModelForm):
    class Meta:
        model = br
        fields = ('title', 'content', )


class FormRegistration(UserCreationForm):
    
    class Meta:
        model = AdvUser
        fields = [ 'username', 'email', 'password1',  'password2']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ExtraInformationForm(forms.ModelForm):
    class Meta:
        model = ExtraInformation
        fields = ['e_inf', 'age', 'gender', 'image',]


class CustomPasswordResetForm(PasswordResetForm):
    pass


class SerarchRecordForm(forms.ModelForm):
    class Meta:
        model = SerarchRecord
        fields = ['value']

class ImagesAdminForm(forms.ModelForm):
    class Meta:
        model = ImagesAdmin
        fields = ['image']