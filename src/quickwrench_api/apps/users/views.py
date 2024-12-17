from typing import Mapping

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer


class RegisterAPIView(APIView):
    permission_classes = []
    serializer_class = RegisterSerializer

    def post(self, request: Request):
        data: Mapping = request.data
        serializer: RegisterSerializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
