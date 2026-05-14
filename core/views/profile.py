from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import User
from rest_framework.request import Request
from core.utilities import verify_request
from test.settings import TOKEN_LIFETIME

@api_view(['GET', 'PUT', 'DELETE'])
@verify_request
def profile(request : Request) -> Response:
    match request.method:
        case 'PUT':
            return PUT_profile__(request=request)
        case 'DELETE':
            return DELETE_profile__(request=request)
        case 'GET' | _:
            return GET_profile__(request=request)

def GET_profile__(request : Request) -> Response:
    assert isinstance(request.user, User)

    data = {
        'forename': request.user.forename,
        'patronymic': request.user.patronymic,
        'surname': request.user.surname,
        'email': request.user.email
    }

    return Response(data=data, status=status.HTTP_200_OK)

def PUT_profile__(request : Request) -> Response:
    assert isinstance(request.user, User)

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
    
    request.user.forename = forename
    request.user.patronymic = patronymic
    request.user.surname = surname
    request.user.save()

    return Response(status=status.HTTP_200_OK)

def DELETE_profile__(request : Request):
    assert isinstance(request.user, User)

    request.user.is_active = False

    request.user.save()

    return Response(
        {'message': f'User was restorably deactivated, last access token will be expired in {TOKEN_LIFETIME}'},
        status=status.HTTP_205_RESET_CONTENT
    )