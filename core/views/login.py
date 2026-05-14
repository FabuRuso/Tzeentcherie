from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from core.models import User, RoleAssignment
import bcrypt
from core.utilities import gen_token


@api_view(['POST'])
def login(request : Request) -> Response:
    email = request.data.get('email')
    password = request.data.get('password')

    if (
        not email or
        not password
    ):
        return Response(
            {'error': '"email" and "password" are required fields to log in'},
            status=status.HTTP_400_BAD_REQUEST
        )
    true_user : User
    try:
        true_user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': 'There is no registered user with such e-mail'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if not true_user.is_active:
        return Response(
            {'error': 'This user was deactivated'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    assert isinstance(true_user.password_hs, str)
    true_password_hs = true_user.password_hs.encode('utf-8')
    
    if not bcrypt.checkpw((password + email).encode('utf-8'), true_password_hs):
        return Response(
            {'error': 'Wrong password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response(
        {'access_token': gen_token(true_user.email)},
        status=status.HTTP_200_OK
    )