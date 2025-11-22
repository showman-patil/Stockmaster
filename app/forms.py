from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    """Allow users to login using username OR email address."""

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # If username looks like an email, try to resolve to username
        if username and '@' in username:
            try:
                user_obj = User.objects.filter(email__iexact=username).first()
                if user_obj:
                    # replace the username value with the user's username so authenticate() can succeed
                    self.cleaned_data['username'] = user_obj.username
            except Exception:
                pass

        return super().clean()
