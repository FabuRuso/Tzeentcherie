from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from core.models import User
from core.utilities import get_user_role

def user_exists(func):
    def wrapper(request : Request, email : str) -> Response:
        assert isinstance(request.user, User)
        user : User

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'User with such e-mail does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if user == request.user:
            return Response(
                {'error': 'Self moderating is not allowed'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        object_user_role = get_user_role(user=user)
        subject_user_role = get_user_role(user=request.user)
        assert subject_user_role is not None

        if object_user_role is not None:
            if (object_user_role.god_perm) and (not subject_user_role.god_perm):
                return Response(
                    {'error': 'Only another god-mode user is allowed to operate'},
                    status=status.HTTP_403_FORBIDDEN
                )

        return func(request, email, user)

@user_exists
def PUT_users_act__(request : Request, email : str, user : User) -> Response:
    if user is None:
        user = User.objects.get(email=email)

    forename = request.data.get('forename')
    patronymic = request.data.get('patronymic', '')
    surname = request.data.get('surname')

    if (
        not forename or
        not surname
    ):
        return Response(
            {'error': '"forename" and "surname" are required fields'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user.forename = forename
    user.patronymic = patronymic
    user.surname = surname

    user.save()
    
    return Response(status=status.HTTP_200_OK)

def PATCH_users_act__(request : Request, email : str, user : User) -> Response:
    if user is None:
        user = User.objects.get(email=email)
    
    user.is_active = False

    user.save()

    return Response(status=status.HTTP_200_OK)

def DELETE_users_act__(request : Request, email : str, user : User) -> Response:
    if user is None:
        user = User.objects.get(email=email)

    user.delete()

    return Response(status=status.HTTP_200_OK)

def GET_users_act__(request : Request, email : str, user : User) -> Response:
    if user is None:
        user = User.objects.get(email=email)

    return Response(
        {
            'forename': user.forename,
            'patronymic': user.patronymic,
            'surname': user.surname,
            'email': user.email
        },
        status=status.HTTP_200_OK
    )