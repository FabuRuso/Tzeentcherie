from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from core.models import Tzeentcherie, User
from core.utilities import get_surname_f_p, get_full_name
from typing import Any

def full_list_unsigned__(request : Request, offset : int = 0) -> Response:
    tzeentcheries_queryset = Tzeentcherie.objects.select_related('owner').order_by('-created_at')[offset:offset+100]

    tzeentcheries_list : list[dict[str, Any]] = []
    for t_instance in tzeentcheries_queryset:
        owner : User = t_instance.owner
        assert isinstance(owner, User)

        tzeentcheries_list.append({
            'title': t_instance.title,
            'created_at': t_instance.created_at,
            'owner': {
                'fullname': get_surname_f_p(user=owner)
                }
            })

    return Response(
        {'list': tzeentcheries_list},
        status=status.HTTP_200_OK
    )

def full_list_signed__(request : Request, offset : int = 0) -> Response:
    tzeentcheries_queryset = Tzeentcherie.objects.select_related('owner').order_by('-created_at')[offset:offset+100]

    tzeentcheries_list : list[dict[str, Any]] = []
    for t_instance in tzeentcheries_queryset:
        owner : User = t_instance.owner
        assert isinstance(owner, User)

        tzeentcheries_list.append({
            'title': t_instance.title,
            'description': t_instance.description,
            'created_at': t_instance.created_at,
            'owner': {
                'fullname': get_full_name(user=owner),
                'email': owner.email,
                'forename': owner.forename,
                'patronymic': owner.patronymic,
                'surname': owner.surname
            }
            })

    return Response(
        {'list': tzeentcheries_list},
        status=status.HTTP_200_OK
    )