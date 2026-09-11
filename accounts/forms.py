from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "elektron.pochta@example.com"})
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ismingiz (ixtiyoriy)"})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Familiyangiz (ixtiyoriy)"})
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Foydalanuvchi nomi (login)"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ["password1", "password2"]:
            if fieldname in self.fields:
                self.fields[fieldname].widget.attrs["class"] = "form-control"
                self.fields[fieldname].widget.attrs["placeholder"] = "Parolni kiriting"


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Foydalanuvchi nomi"
        })
        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Parol"
        })

