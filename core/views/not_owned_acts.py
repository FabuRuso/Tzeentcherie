from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from core.models import Tzeentcherie

def not_owned_tzeentcherie_exists(func):
    def wrapper(request : Request, title : str, *args, **kwargs) -> Response:
        tzeentcherie : Tzeentcherie

        try:
            tzeentcherie = Tzeentcherie.objects.get(title=title)
        except Tzeentcherie.DoesNotExist:
            return Response(
                {'error': 'Tzeentcherie with such title does not yet exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if tzeentcherie.owner == request.user:
            return Response(
                {'error': 'Itself owned Tzeentcherie was tried'},
                status=status.HTTP_421_MISDIRECTED_REQUEST
            )

        return func(request, title, tzeentcherie, *args, **kwargs)

@not_owned_tzeentcherie_exists
def PUT_not_owned_act__(request : Request, title : str, tzeentcherie : Tzeentcherie) -> Response:
    if tzeentcherie is None:
        tzeentcherie = Tzeentcherie.objects.get(title=title)

    tzeentcherie.description = request.data.get('description', '')

    tzeentcherie.save()

    return Response(status=status.HTTP_200_OK)

@not_owned_tzeentcherie_exists
def DELETE_not_owned_act__(request : Request, title : str, tzeentcherie : Tzeentcherie) -> Response:
    if tzeentcherie is None:
        tzeentcherie = Tzeentcherie.objects.get(title=title)

    tzeentcherie.delete()

    return Response(status=status.HTTP_200_OK)

@not_owned_tzeentcherie_exists
def GET_not_owned_act__(request : Request, title : str, tzeentcherie : Tzeentcherie) -> Response:
    if tzeentcherie is None:
        tzeentcherie = Tzeentcherie.objects.get(title=title)
        
    return Response(
        {
            'title': tzeentcherie.title,
            'description': tzeentcherie.description
            },
            status=status.HTTP_200_OK
    )