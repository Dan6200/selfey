from django.contrib.auth.backends import ModelBackend
from rest_framework.exceptions import AuthenticationFailed
from .email_backend import EmailBackend
backend = EmailBackend()

def login_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            registered_user = backend.authenticate(email=email)

            if registered_user is not None:
                return {
                    'username': user.username,
                    'email': user.email,
                    'tokens': user.tokens()
                }

    raise AuthenticationFailed('Google account not registered')
