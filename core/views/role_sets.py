from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from core.models import User, Role, RoleAssignment
from core.utilities import get_user_role

def PUT_role_set__(request : Request, email : str) -> Response:
    user : User

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': 'No user with such e-mail exists'}
        )
    
    role_name = request.data.get('role_name')

    if not role_name:
        return Response(
            {'error': '"role_name" is a required field'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    role : Role

    try:
        role = Role.objects.get(role_name=role_name)
    except Role.DoesNotExist:
        return Response(
            {'error': 'No role with such name exists'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        assignment = RoleAssignment.objects.get(user=user)
        assignment.role = role
        assignment.save()
        return Response(status=status.HTTP_200_OK)
    except RoleAssignment.DoesNotExist:
        RoleAssignment.objects.create(user=user, role=role)
        return Response(status=status.HTTP_201_CREATED)

def GET_role_set__(request : Request, email : str) -> Response:
    user : User

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': 'No user with such e-mail exists'}
        )
    
    try:
        assignment = RoleAssignment.objects.get(user=user)
        assert isinstance(assignment.role, Role)
        return Response(
            {'role_name': assignment.role.role_name},
            status=status.HTTP_200_OK
        )
    except RoleAssignment.DoesNotExist:
        return Response(
            {'role_name': None},
            status=status.HTTP_204_NO_CONTENT
        )