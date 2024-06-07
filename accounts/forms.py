from django import forms
from django.forms import ModelForm
from .models import Profile, Message
class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control rounded-pill', 'placeholder': 'имя'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control rounded-pill', 'placeholder': 'пароль'}
        )
    )
class UserRegistrationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control rounded-pill', 'placeholder': 'почта'}
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control rounded-pill', 'placeholder': 'имя'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control rounded-pill', 'placeholder': 'пароль'}
        )
    )
class EditProfileForm(ModelForm):
    photo = forms.ImageField(required=False, widget=forms.FileInput)
    
    class Meta:
        model = Profile
        fields = ['photo', 'about', 'fname', 'lname', 'pronouns', 'website']
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'about':
                visible.field.widget.attrs['class'] = 'edit-profile-input form-control about-input'
            else:
                visible.field.widget.attrs['class'] = 'edit-profile-input form-control rounded-pill'
                
# class MessageForm(ModelForm):
#     class Meta:
#         model = Message
#         fields = ['message']
#         labels = {'message': ""}    

class MessageForm(ModelForm):
    # recipient_username = forms.CharField(max_length=150)
    # recipient_username = forms.CharField(max_length=150)
    class Meta:
        model = Message
        # fields = ['name', 'email', 'subject', 'body', 'recipient_username']
        fields = ['subject', 'body']
 
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
 
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})