from rest_framework.decorators import api_view
from rest_framework.response   import Response
from rest_framework.request    import Request
from rest_framework            import status
from core.models import User, Role, RoleAssignment
from core.utilities import verify_request, get_user_role

from core.views.owned_acts     import *
from core.views.not_owned_acts import *
from core.views.users_acts     import *
from core.views.role_sets      import *
from core.views.role_acts      import *
from core.views.full_list_acts import *

def check_perm__(perm : bool, method, pair : tuple[Request, str]) -> Response:
    if not perm:
        return Response(status=status.HTTP_403_FORBIDDEN)
    return method(*pair)

@api_view(['POST', 'PUT', 'DELETE', 'GET'])
@verify_request
def owned_act(request : Request, title : str) -> Response:
    assert isinstance(request.user, User)

    role = get_user_role(user=request.user)
    if not isinstance(role, Role):
        return Response(
            {'error': 'No role was assigned'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    match request.method:
        case 'POST':
            return check_perm__(role.post_owned_perm or role.god_perm, POST_owned_act__, (request, title))
        case 'PUT':
            return check_perm__(role.put_owned_perm or role.god_perm, PUT_owned_act__, (request, title))
        case 'DELETE':
            return check_perm__(role.delete_owned_perm or role.god_perm, DELETE_owned_act__, (request, title))
        case 'GET' | _:
            return check_perm__(True, GET_owned_act__, (request, title))


@api_view(['PUT', 'DELETE', 'GET'])
@verify_request
def not_owned_act(request : Request, title : str) -> Response:
    assert isinstance(request.user, User)

    role = get_user_role(user=request.user)
    if not isinstance(role, Role):
        return Response(
            {'error': 'No role was assigned'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    match request.method:
        case 'PUT':
            return check_perm__(role.put_not_owned_perm or role.god_perm, PUT_not_owned_act__, (request, title))
        case 'DELETE':
            return check_perm__(role.delete_not_owned_perm or role.god_perm, DELETE_not_owned_act__, (request, title))
        case 'GET' | _:
            return check_perm__(True, GET_not_owned_act__, (request, title))


@api_view(['PUT', 'PATCH', 'DELETE', 'GET'])
@verify_request
def users_act(request : Request, email : str) -> Response:
    assert isinstance(request.user, User)

    role = get_user_role(user=request.user)
    if not isinstance(role, Role):
        return Response(
            {'error': 'No role was assigned'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    match request.method:
        case 'PUT':    # <==  editing of user info
            return check_perm__(role.put_users_perm or role.god_perm, PUT_users_act__, (request, email))
        case 'PATCH':  # <== 'soft' deactivation,  saving in db
            return check_perm__(role.deactivate_users_perm or role.god_perm, PATCH_users_act__, (request, email))
        case 'DELETE': # <==  full  deletion,      removing from db
            return check_perm__(role.delete_users_perm or role.god_perm, DELETE_users_act__, (request, email))
        case 'GET' | _:
            return check_perm__(True, GET_users_act__, (request, email))

@api_view(['PUT', 'GET'])
@verify_request
def role_set(request : Request, email : str) -> Response:
    assert isinstance(request.user, User)

    object_user_role = get_user_role(email=email)
    subject_user_role = get_user_role(user=request.user)
    if subject_user_role is None:
        return Response(
            {'error': 'No role was assigned'},
            status=status.HTTP_404_NOT_FOUND
        )

    if object_user_role is not None:
        if (object_user_role.god_perm) and (not subject_user_role.god_perm):
            return Response(
                {'error': 'Only another god-mode user is allowed to operate'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    match request.method:
        case 'PUT':
            return check_perm__(subject_user_role.edit_roles_perm or subject_user_role.god_perm, PUT_role_set__, (request, email))
        case 'GET' | _:
            return check_perm__(True, GET_role_set__, (request, email))


@api_view(['PUT', 'DELETE', 'GET'])
@verify_request
def role_act(request, role_name : str):
    assert isinstance(request.user, User)

    role = get_user_role(user=request.user)
    if not isinstance(role, Role):
        return Response(
            {'error': 'No role was assigned'},
            status=status.HTTP_404_NOT_FOUND
        )

    match request.method:
        case 'PUT':
            return check_perm__(role.edit_roles_perm or role.god_perm, PUT_role_act__, (request, role_name))
        case 'DELETE':
            return check_perm__(role.edit_roles_perm or role.god_perm, DELETE_role_act__, (request, role_name))
        case 'GET' | _:
            return check_perm__(True, GET_role_act__, (request, role_name))


@api_view(['GET'])
def full_list(request : Request) -> Response:
    offset : int = request.data.get('offset', 0)

    match request.user:
        case None:
            return full_list_unsigned__(request, offset)
        case _:
            return full_list_signed__(request, offset)