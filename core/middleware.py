from django.utils.deprecation import MiddlewareMixin
from core.models import User
from core.utilities import unravel_token

class AccessTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = None
        
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return
        
        access_token = auth_header.split()[1]

        unraveled = unravel_token(access_token)

        if unraveled[0]:
            try:
                request.user = User.objects.get(email=unraveled[1]['email'], is_active=True)
            except User.DoesNotExist:
                pass