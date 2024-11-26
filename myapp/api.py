from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken
from rest_framework.exceptions import NotAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User


class UserAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    
    
    def get (self, request):
        user = request.user
        
        
        if not user.is_authenticated:
            raise NotAuthenticated()
        
        return Response({
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            
        })
        
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        
        if username and password:
            if User.objects.filter(username=username).exists():
                return Response({"error": "User already exists"}, status=401)
            
            user = User.objects.create_user(username=username, password=password)
            
            refresh = RefreshToken.for_user(user)
            return Response({
                "detail": "User Created Successfully!",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },status=201)
            
        return Response({
            "error": "username and password must be provided"
            }, status=400)
    
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token = request.data.get('refresh')
    
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully Logged out!"}, status=200)
        except Exception as e:
            return Response({"error": "Invalid token."}, status=400)
    else:
        return Response({"error": "Refresh token is required."}, status=400)