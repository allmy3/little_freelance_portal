from django import forms
from  django.contrib.auth.forms import UserCreationForm
from  django.contrib.auth import get_user_model

from .models import Profile, Rate, ResponseToCompany

User = get_user_model()


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'auth_form__field top-three-three'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Логин', 'class': 'auth_form__field top-three-three'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError(f"Пользователь с логином {username} не найден в системе!")
        if not user.check_password(password):
            raise forms.ValidationError("Неверный пароль!!!")
        return self.cleaned_data


class RegisterForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Логин', 'class': 'auth_form__field top-three-three'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Эл.Почта', 'class': 'auth_form__field top-three-three'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'auth_form__field top-three-three'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повтор пароля', 'class': 'auth_form__field top-three-three'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ChangeUserPasswordForm(forms.ModelForm):

    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'auth_form__field top-three-three', 'placeholder': 'Старый пароль'}), required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'auth_form__field top-three-three', 'placeholder': 'Новый пороль'}),required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'auth_form__field top-three-three', 'placeholder': 'Подтверждение нового пароля'}), required=True)

    class Meta:
        model = User
        fields = ['id', 'old_password', 'new_password', 'confirm_password']

    def clean(self):
        super(ChangeUserPasswordForm, self).clean()
        id = self.cleaned_data['id']
        old_password = self.cleaned_data['old_password']
        new_password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_password']
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] =self.error_class(['Old password do not match.'])
        if new_password != confirm_password:
            self._errors['new_password'] =self.error_class(['Passwords do not match.'])
        return self.cleaned_data


class ChangeProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['free_lancer_status', 'company']


class GiveRateForm(forms.ModelForm):

    class Meta:
        model = Rate
        fields = ['description_for_rate_report', 'number_of_value']


class SendResComForm(forms.ModelForm):

    class Meta:
        model = ResponseToCompany
        fields = ['text']