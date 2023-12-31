from .email_backend import EmailBackend
from .models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed
from dotenv import load_dotenv
load_dotenv('.env')

backend = EmailBackend()
def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(email=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = backend.authenticate(email=email, password=os.getenv('SOCIAL_SECRET'))


            if registered_user is not None:
                return {
                    'username': registered_user.username,
                    'id': registered_user.id,
                    'email': registered_user.email,
                    'tokens': registered_user.tokens()}
            else:
                user = {
                    'username': generate_username(name), 'email': email}
                user = User.objects.create_user(**user)
                user.is_verified = True
                user.auth_provider = provider
                user.save()

                new_user = backend.authenticate(email=email)
                return {
                    'email': new_user.email,
                    'id': new_user.id,
                    'username': new_user.username,
                    'tokens': new_user.tokens()
                }


        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'username': generate_username(name), 'email': email,
            'password': os.getenv('SOCIAL_SECRET')}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        return {
            'email': user.email,
            'username': user.username,
            'id': user.id,
            'tokens': user.tokens()
        }
