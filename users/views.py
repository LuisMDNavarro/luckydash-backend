from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from luckydash import settings
from tenants.mixins import TenantMixin
from users.models import CustomUser
from users.serializers import CustomUserSerializer, RegisterSerializer


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Usuario creado con éxito"}, status=HTTP_201_CREATED
            )

        return Response(
            {
                "errors": serializer.errors,
            },
            status=HTTP_400_BAD_REQUEST,
        )


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access = response.data.get("access")
        refresh = response.data.get("refresh")
        new_response = self.response = Response({"message": "Login exitoso"})
        new_response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=False,  # UPDATE: True para HTTPS
            samesite="Lax",
            max_age=3600,
        )

        new_response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=False,  # UPDATE: True para HTTPS
            samesite="Lax",
            max_age=86400,
        )
        return new_response


class CookieTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            raise AuthenticationFailed("Refresh Token es requerido")

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token
            user = CustomUser.objects.get(id=refresh["user_id"])
            if settings.SIMPLE_JWT["ROTATE_REFRESH_TOKENS"]:
                refresh.blacklist()
                new_refresh = RefreshToken.for_user(user)
        except (CustomUser.DoesNotExist, Exception):
            raise AuthenticationFailed("Refresh Token invalido o expirado")

        response = Response({"message": "Token actualizado"})

        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=False,  # UPDATE: True para HTTPS
            samesite="Lax",
            max_age=3600,
        )
        response.set_cookie(
            key="refresh_token",
            value=new_refresh,
            httponly=True,
            secure=False,  # UPDATE: True para HTTPS
            samesite="Lax",
            max_age=86400,
        )
        return response


class CustomUserViewSet(TenantMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        return CustomUser.objects.filter(uid=self.request.user.uid).distinct()
