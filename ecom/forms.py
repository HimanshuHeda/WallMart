
from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        
    
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = ''
        self.fields['username'].label = 'User Name'
        self.fields['username'].help_text = None

    #     self.fields['password1'].widget.attrs['class'] = 'form-control'
    #     self.fields['password1'].widget.attrs['placeholder'] = ''
    #     self.fields['password1'].label = 'Password'
    #     self.fields['password1'].help_text = None

    #     self.fields['password2'].widget.attrs['class'] = 'form-control'
    #     self.fields['password2'].widget.attrs['placeholder'] = ''
    #     self.fields['password2'].label = 'Confirm Password'
    #     self.fields['password2'].help_text = None





    #     class RegistrationForm(forms.Form):
    # username = forms.CharField()
    # password = forms.CharField(widget=forms.PasswordInput)

    # def save(self):
    #     # Use the custom manager from the custom user model
    #     User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'])