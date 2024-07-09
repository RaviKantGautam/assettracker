from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class UserAuthenticationForm(AuthenticationForm):
    '''
    Custom authentication form
    '''
    email = forms.EmailField(required=True, label=_('Email'), widget=forms.EmailInput(
        attrs={'autofocus': True, 'placeholder': _('Email'), 'class': 'form-control'}))
    password = forms.CharField(required=True, label=_('Password'), widget=forms.PasswordInput(
        attrs={'placeholder': _('Password'), 'class': 'form-control'}))
    remember_me = forms.BooleanField(required=False, label=_(
        'Remember me'), widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        # Remove username field
        self.fields.pop('username')

    def clean(self):
        super(UserAuthenticationForm, self).clean()
        email = self.cleaned_data.get('email')
        remember_me = self.cleaned_data.get('remember_me')

        # Set session expiry to 2 weeks if remember_me is checked
        if remember_me:
            # Set session expiry to 2 weeks
            self.request.session.set_expiry(settings.SESSION_COOKIE_AGE)
        else:
            self.request.session.set_expiry(0)

        # Authenticate user
        if email:
            self.user_cache = authenticate(
                self.request,
                username=email,
                password=self.cleaned_data.get('password')
            )
            # Check if user is authenticated
            if self.user_cache is None:
                raise forms.ValidationError(
                    'Invalid email or password'
                )
        return self.cleaned_data
