from typing import Mapping

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quickwrench_api.apps.workshops.serializers import WorkshopSerializers


class WorkshopAPIView(APIView):
    permission_classes = []
    serializer_class = WorkshopSerializers

    def post(self, request: Request):
        data: Mapping = request.data
        serialzer: WorkshopSerializers = WorkshopSerializers(data=data)
        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data, status=status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
