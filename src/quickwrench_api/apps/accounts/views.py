from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AccountSerializer


class AccountDetailsAPIView(APIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
