from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from .serializer import UserSerializer, CustomTokenObtainPairSerializer
from .serializer import UserSerializer


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class TokenPairSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


class RegisterResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = UserSerializer()


class LogoutRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


@extend_schema(
    tags=['auth'],
    request=UserSerializer,
    responses={
        201: RegisterResponseSerializer,
        400: OpenApiResponse(description='Validation errors'),
    },
    summary='Register a new user and return JWT pair',
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['auth'],
    request=LoginRequestSerializer,
    responses={
        200: TokenPairSerializer,
        400: OpenApiResponse(
            response=inline_serializer(
                name='LoginErrorResponse',
                fields={'error': serializers.CharField()},
            ),
            description='Invalid credentials',
        ),
    },
    summary='Authenticate with email + password, return JWT pair',
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get("email")  
    password = request.data.get("password")
    user = authenticate(email=email, password=password)  

    if user:
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


# Novo view para token customizado
# Esta view é responsável por processar as solicitações de login (autenticação) e retornar tokens JWT para os usuários.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Novo endpoint para logout
@extend_schema(
    tags=['auth'],
    request=LogoutRequestSerializer,
    responses={
        205: OpenApiResponse(
            response=inline_serializer(
                name='LogoutSuccessResponse',
                fields={'success': serializers.CharField()},
            ),
            description='Refresh token successfully blacklisted',
        ),
        400: OpenApiResponse(
            response=inline_serializer(
                name='LogoutErrorResponse',
                fields={'error': serializers.CharField()},
            ),
            description='Invalid or missing refresh token',
        ),
    },
    summary='Blacklist the provided refresh token',
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"success": "Logout realizado com sucesso"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
