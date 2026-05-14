from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

@api_view(['GET'])
def hello(request : Request) -> Response:
    return Response({"message": "Hello World!"}, status=status.HTTP_418_IM_A_TEAPOT)
