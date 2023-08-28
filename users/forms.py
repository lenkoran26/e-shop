from django.contrib.auth.models import User
from django import forms  ## Для переопределения полей в формах
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UsernameField

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, error_messages={'required': 'Пожалуйста заполните поле!'})
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email') ## Поля
        help_texts = {
            'username': 'Только буквы, цыфры и символы @/./+/-/_',
        }

        verbose_name = {
            'username': 'login',
        }

        labels = {
            'username': 'Логин',
            'first_name': 'Имя пользователя',
            'email': 'Электронная почта',
        }

        widgets = {
            'username': forms.TextInput,
            'email': forms.EmailInput,
            'first_name': forms.TextInput,
        }

    def clean_password2(self):  ## Важно чтобы начиналось со слова clean_<имя поля>
        cd = self.cleaned_data  ## В момент валидации создается словарик
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')  ## raise в "ручном" режиме генерирует исключение
        return cd['password2']

class AuthForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True}),
        label=_("Логин"),
    )
    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Пожалуйста введите коректные логин и пароль. Обратите внимание на то, что! "
            "поля могут быть чувствительны к регистру."
        ),
        "inactive": _("Этот аккаунт заблокирован."),
    }