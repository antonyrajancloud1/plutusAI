from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class QueryParamTokenAuthentication(TokenAuthentication):
    """
    Custom authentication class that retrieves the token from a URL parameter instead of the header.
    """

    def authenticate(self, request):
        # Look for the token in the 'token' query parameter
        token = request.query_params.get('token')

        if not token:
            return None  # No token found, authentication fails silently (falls back to other auth methods)

        # Proceed with the standard token authentication process
        return self.authenticate_credentials(token)
