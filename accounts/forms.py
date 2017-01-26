from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext, ugettext_lazy as _

from .models import Account


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC',
            super(UsernameField, self).to_python(value))


class UserCreationForm(forms.ModelForm):
    """ A form that creates a user, with no privileges,
        from the given username and password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = Account
        fields = ("email",)
        field_classes = {'email': UsernameField}

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': ''})

    def clean_password2(self):
        """ validate the password confirmation value
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('email')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        
        return user


class LoginForm(forms.Form):
    """ login form
    """
    error = "Email or Password is incorrect"

    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        """ validate user's credentials
        """
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if not (email or password):
            raise forms.ValidationError(self.error, code="invalid_login")

        self.user_cache = authenticate(email=email, password=password)
        if self.user_cache is None or \
           not self.user_cache.is_active:
            raise forms.ValidationError(self.error, code="invalid_login")

        return self.cleaned_data


class SignupForm(forms.ModelForm):
    """ signup form
    """
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        email = self.cleaned_data.get('email') 
        """ Check if Email is already Exist 
        """
        qs = Account.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email address already exist")     
        if not password:
            raise forms.ValidationError("Password is required")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return self.cleaned_data

    class Meta:
        model = Account
        fields = (
            'email',
            'first_name',
            'last_name',
            'birthdate',
            'gender',
            'contact',
            'address',
            'position',
            'job_title',
            'password',
            'confirm_password',
        )

    def save(self, commit=True, *args, **kwargs):
        instance = super(SignupForm, self).save(commit=False)
        """
            username = email
        """
        instance.username = self.cleaned_data.get('email')
        if commit:
            instance.set_password(self.cleaned_data.get('password'))
            instance.save()

        return instance