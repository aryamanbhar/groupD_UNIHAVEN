from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken


def create_custom_token(user, university, role):
    token = AccessToken.for_user(user)  
    token["university"] = university   
    token["role"] = role
    return str(token) 

def validate_auth_token(token_key):
    """
    Validate the provided authentication token.
    """
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return None

def revoke_auth_token(user):
    """
    Revoke the authentication token for the given user.
    """
    try:
        token = Token.objects.get(user=user)
        token.delete()
    except Token.DoesNotExist:
        pass