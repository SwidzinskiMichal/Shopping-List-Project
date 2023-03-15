from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password',)

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password and password_confirmation and password != password_confirmation:
            raise ValidationError("Passwords don't match")

        return password_confirmation

    def save(self, commit=True):
        user = get_user_model().objects.create_user(
            email= self.cleaned_data.get('email'),
            username=self.cleaned_data.get('username'),
            password=self.cleaned_data.get('password'),
        )

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={
            'name': 'username',
            'placeholder': 'Email'
        })
    )

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['username', 'password']