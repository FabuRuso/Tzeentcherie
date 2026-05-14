from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import User, Role, RoleAssignment
from rest_framework.request import Request
from core.utilities import verify_request
from test.settings import DEBUG
from test.settings import DEBUG_RELEASED
import bcrypt

@api_view(['PUT'])
def release_debug_placeholders(request : Request) -> Response:
    global DEBUG_RELEASED
    match (DEBUG, DEBUG_RELEASED):
        case (True, False):
            DEBUG_RELEASED = True
            return DEBUG_PH__(request)
        case (_, True):
            return Response(
                {'error': 'Debug-mod was already released'},
                status=status.HTTP_409_CONFLICT
            )
        case (False, _):
            return Response(
                {'error': 'Debug-mod is offline'},
                status=status.HTTP_410_GONE
            )
        case _:
            return Response(
                {}
            )

def DEBUG_PH__(request : Request) -> Response:
    user = User.objects.create(
        email='admin@himmel.test',
        forename='Herr',
        surname='Goetze',
        password=bcrypt.hashpw(
            password=('admin' + 'admin@himmel.test').encode('utf-8'),
            salt=bcrypt.gensalt()
            ).decode('utf-8'))
    role = Role.objects.create(
        role_name='admin',
        god_perm=True,
        edit_roles_perm=True
        )
    RoleAssignment.objects.create(role=role, user=user)

    user = User.objects.create(
        email='moderator@admins.test',
        forename='Dr',
        surname='Who',
        password=bcrypt.hashpw(
            password=('moder' + 'moderator@admins.test').encode('utf-8'),
            salt=bcrypt.gensalt()
            ).decode('utf-8'))
    role = Role.objects.create(
        role_name='moder',
        put_not_owned_perm=True,
        delete_not_owned_perm=True)
    RoleAssignment.objects.create(role=role, user=user)
    
    return Response(status=status.HTTP_201_CREATED)