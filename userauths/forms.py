from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "ПІБ"}))
    telephone = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "+380..."})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Підтвердження паролю"})
    )

    class Meta:
        model = User
        fields = ["full_name", "email", "telephone"]


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Повне імя та прізвище"})
    )
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Про себе"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Телефон"}))

    class Meta:
        model = Profile
        fields = ["full_name", "bio", "phone"]


class UserUpdateForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ["first_name", "full_name", "telephone"]

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")

        return cleaned_data
