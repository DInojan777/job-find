from .models import *
from users.models import *
from rest_framework.authtoken.models import Token

def get_user_token(username):
    try:
        user=User.objects.get(username=username)
        try:
            token=Token.objects.get(user=user)
            return token.key
        except:
            token=Token.objects.create(user=user)
            return token.key
    except:
        return None

def get_active_user(**kargs):
    try:
        return UserAuthentication.objects.get(**kargs)
    except:
        return None

def getuser_by_mobile(username):
    try:
        ep = UserPersonalInfo.objects.get(mobile_number=username)
        return ep.user
    except:
        return None

