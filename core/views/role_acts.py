from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from core.models import Role
from django.forms.models import model_to_dict

def PUT_role_act__(request : Request, role_name : str) -> Response:
    role : Role

    data : dict = request.data

    god_perm = data.get('god_perm', False)
    edit_roles_perm = data.get('edit_roles_perm', False)
    post_owned_perm = data.get('post_owned_perm', False)
    put_owned_perm = data.get('put_owned_perm', False)
    delete_owned_perm = data.get('delete_owned_perm', False)
    put_not_owned_perm = data.get('put_not_owned_perm', False)
    delete_not_owned_perm = data.get('delete_not_owned_perm', False)
    put_users_perm = data.get('put_users_perm', False)
    deactivate_users_perm = data.get('deactivate_users_perm', False)
    delete_users_perm = data.get('delete_users_perm', False) 

    try:
        role = Role.objects.get(role_name=role_name)

        role.god_perm = god_perm
        role.edit_roles_perm = edit_roles_perm
        role.post_owned_perm = post_owned_perm
        role.put_owned_perm = put_owned_perm
        role.delete_owned_perm = delete_owned_perm
        role.put_not_owned_perm = put_not_owned_perm
        role.delete_not_owned_perm = delete_not_owned_perm
        role.put_users_perm = put_users_perm
        role.deactivate_users_perm = deactivate_users_perm
        role.delete_users_perm = delete_users_perm

        role.save()

        return Response(
            {'message': f'Role "{role_name}" was updated'},
            status=status.HTTP_200_OK
        )
    except Role.DoesNotExist:

        Role.objects.update_or_create(
            role_name=role_name,
            defaults={
                'god_perm': god_perm,
                'edit_roles_perm': edit_roles_perm,
                'post_owned_perm': post_owned_perm,
                'put_owned_perm': put_owned_perm,
                'delete_owned_perm': delete_owned_perm,
                'put_not_owned_perm': put_not_owned_perm,
                'delete_not_owned_perm': delete_not_owned_perm,
                'put_users_perm': put_users_perm,
                'deactivate_users_perm': deactivate_users_perm,
                'delete_users_perm': delete_users_perm}
        )

        return Response(
            {'message': f'New role "{role_name}" was created'},
            status=status.HTTP_201_CREATED
        )

def DELETE_role_act__(request : Request, role_name : str) -> Response:
    try:
        Role.objects.get(role_name=role_name).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Role.DoesNotExist:
        return Response(
            {'error': 'No role with such name exists'},
            status=status.HTTP_404_NOT_FOUND
        )

def GET_role_act__(request : Request, role_name : str) -> Response:
    try:
        role = Role.objects.get(role_name=role_name)
        return Response(
            model_to_dict(role),
            status=status.HTTP_200_OK
            )
    except Role.DoesNotExist:
        return Response(
            {'error': 'No role with such name exists'},
            status=status.HTTP_404_NOT_FOUND
        )