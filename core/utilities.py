from test.settings import SECRET_KEY, TOKEN_LIFETIME
import jwt
from datetime import datetime
from typing import Any
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from core.models import User, Role, RoleAssignment


def gen_token(email) -> str:
    payload = {
        'email': email,
        'exp': datetime.utcnow() + TOKEN_LIFETIME,
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256')

def unravel_token(access_token) -> tuple[bool, dict[str, Any]]:
    payload : dict[str, Any] = {}
    valid : bool = True
    try:
        payload = jwt.decode(access_token, key=SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError | jwt.InvalidSignatureError:
        valid = False
    return (valid, payload)

def verify_request(func):
    @wraps(func)
    def wrapper(request : Request, *args, **kwargs):
        if not request.user:
            return Response(
                {'error': 'Valid access token is required in the header'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return func(request, *args, **kwargs)
    return wrapper

def get_user_role(email : str | None = None, user : User | None = None) -> Role | None:
    assert (email is not None) or (user is not None)
    if user is not None:
        try:
            return RoleAssignment.objects.select_related('role').get(user=user).role
        except RoleAssignment.DoesNotExist:
            return None
    if email is not None:
        try:
            return RoleAssignment.objects.select_related('role').get(user__email=email).role
        except RoleAssignment.DoesNotExist | User.DoesNotExist:
            return None

def get_surname_f_p(user : User | None = None, forename : str = '', patronymic : str = '', surname : str = '') -> str:
    if user is not None:
        forename = user.forename
        patronymic = user.patronymic
        surname = user.surname
    
    if patronymic == '':
        return f"{surname} {forename[0]}."
    else:
        return f"{surname} {forename[0]}. {patronymic[0]}."

def get_full_name(user : User | None = None, forename : str = '', patronymic : str = '', surname : str = '') -> str:
    if user is not None:
        forename = user.forename
        patronymic = user.patronymic
        surname = user.surname
    
    if patronymic == '':
        return f"{surname} {forename}"
    else:
        return f"{surname} {forename} {patronymic}"