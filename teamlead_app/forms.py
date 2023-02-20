from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, DateInput, TextInput

from teamlead_app.models import selected_candidate_interview


class UserRegistrationForm(UserCreationForm):
    group = (
        ("Teamlead", "Teamlead"),
        ("HR", "HR"),
    )

    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(widget=TextInput(attrs={'type': 'number'}))
    user_group = forms.ChoiceField(choices = group)


    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','user_group','phone_number','password1','password2']


#----------------------------------------------------------------------------------------------------------------------------
#Form for scheduling the event (Interviews)

class UpdateForm(forms.Form):
    budget = forms.CharField(max_length=100)


