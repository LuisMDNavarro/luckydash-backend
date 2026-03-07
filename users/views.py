from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

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


class CustomUserViewSet(TenantMixin, ModelViewSet):
    lookup_field = "uid"
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        return CustomUser.objects.filter(uid=self.request.user.uid).distinct()
