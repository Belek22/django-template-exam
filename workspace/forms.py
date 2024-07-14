from django import forms
from news.models import Product, Category, Tag

from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберите категорию'

    class Meta:
        model = Product
        fields = [
            'title',
            'price',
            'image',
            'content',
            'category',
            'tags'
        ]

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'p-2 border rounded-lg w-full', 'placeholder': 'Введите заголовок'}),
            'price': forms.NumberInput(attrs={'class': 'p-2 border rounded-lg w-full', 'placeholder': 'Введите цену'}),
            'image': forms.FileInput(attrs={'accept': 'image/*', 'class': 'p-2 mt-7 w-full'}),
            'content': forms.Textarea(attrs={'class': 'p-2 border rounded-lg w-full', 'placeholder': 'Контент'}),
            'category': forms.Select(attrs={'class': 'p-2 border rounded-lg w-full'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'p-2 border rounded-lg w-full'})
        }


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(
                                   attrs={'class': 'w-full border border-gray-300 rounded-3xl px-4 py-2 mb-4',
                                          'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'w-full border border-gray-300 rounded-3xl px-4 py-2', 'placeholder': 'Введите пароль'}))


class RegisterForm(BaseUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full border border-gray-300 rounded-3xl px-4 py-2 mb-4',
            'placeholder': 'Придумайте пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full border border-gray-300 rounded-3xl px-4 py-2',
            'placeholder': 'Подтвердите пароль'
        })

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        )

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-3xl px-4 py-2 mb-4',
                                                 'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-3xl px-4 py-2 mb-4',
                                                'placeholder': 'Введите фамилию'}),
            'username': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-3xl px-4 py-2 mb-4',
                                               'placeholder': 'Придумайте имя пользователя'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border border-gray-300 rounded-3xl px-4 py-2 mb-4',
                                             'placeholder': 'Введите эл. почту'}),
        }


class ChangeProfileForm(forms.ModelForm):

    # email = forms.EmailField(label='Эл. почта', required=True,
    #                          widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите эл. почту'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-3xl px-4 py-2 mt-2',
                                                 'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-3xl px-4 py-2 mt-2',
                                                'placeholder': 'Введите фамилию'}),
            'username': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-3xl px-4 py-2 mt-2',
                                               'placeholder': 'Имя пользователя'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border border-gray-300 rounded-3xl px-4 py-2 mt-2',
                                             'placeholder': 'Введите эл. почту'}),
        }


class ChangePasswordForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    password = forms.CharField(label='Текущий пароль',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'w-full border border-gray-300 rounded-md px-4 py-2 mb-4 focus:border-blue-500',
                                   'placeholder': 'Введите текущий пароль'}))
    new_password = forms.CharField(label='Новый пароль',
                                   widget=forms.PasswordInput(attrs={
                                       'class': 'w-full border border-gray-300 rounded-md px-4 py-2 mb-4 focus:border-blue-500',
                                       'placeholder': 'Введите новый пароль'}),
                                   validators=[validate_password])
    confirm_password = forms.CharField(label='Подтвердите пароль',
                                       widget=forms.PasswordInput(attrs={
                                           'class': 'w-full border border-gray-300 rounded-md px-4 py-2 mb-4 focus:border-blue-500',
                                           'placeholder': 'Подтвердите пароль'}))

    def clean(self):
        data = self.cleaned_data

        password = data.get('password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        errors = {}

        if not self.user.check_password(password):
            errors['password'] = ['Неправильный пароль']

        if new_password != confirm_password:
            errors['confirm_password'] = ['Пароли не совпадают']

        if len(errors) > 0:
            raise forms.ValidationError(errors)

        return data
