from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser


class TestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
            }
        )


@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Hello LuckyDash"})


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    # serializer_class = UserSerializer
