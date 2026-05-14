from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from core.models import User, Role, RoleAssignment
import bcrypt

@api_view(['POST'])
def register(request : Request) -> Response:
    email = request.data.get('email')
    forename = request.data.get('forename')
    patronymic = request.data.get('patronymic', '')
    surname = request.data.get('surname')
    password = request.data.get('password')
    password_confirm = request.data.get('password_confirm')

    if (
        not email or
        not forename or
        not surname or 
        not password or
        not password_confirm
    ):
        return Response(
            {'error': '"email", "forename", "surname", "password" and "password_confirm" are required fields'},
            status=status.HTTP_400_BAD_REQUEST
            )
    
    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'One User with such e-mail already exists'},
            status=status.HTTP_409_CONFLICT
        )
    
    if password_confirm != password:
        return Response(
            {'error': 'Password was not confirmed'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create(
        email=email,
        forename=forename,
        patronymic=patronymic,
        surname=surname,
        password=bcrypt.hashpw(
            password=(password + email).encode('utf-8'),
            salt=bcrypt.gensalt()
            ).decode('utf-8'))
    DEFAULT_ROLE, _ = Role.objects.get_or_create(role_name='DEFAULT')
    RoleAssignment.objects.create(user=user, role=DEFAULT_ROLE)

    return Response(
        {'message': f'User "{email}" was successfully created'},
        status=status.HTTP_201_CREATED
        )