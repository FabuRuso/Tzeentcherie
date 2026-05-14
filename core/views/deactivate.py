from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from models import User
from rest_framework.request import Request
from core.utilities import verify_request

@api_view(['DELETE'])
@verify_request
def deactivate(request : Request) -> Response:
    assert isinstance(request.user, User)

    request.user.is_active = False
    request.user.save()

    return Response(
        {'message': 'User was deactivated'},
        status=status.HTTP_200_OK
    )
