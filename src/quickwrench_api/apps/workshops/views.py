from typing import Mapping

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category

from .serializers import WorkshopSerializer, CategorySerializer


class CategoryAPIView(APIView):
    permission_classes = []
    serializer_class = CategorySerializer

    def get(self, request):
        category = Category.objects.all()
        if not category.exists():
            return Response(
                {"message": "No category available."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkshopAPIView(APIView):
    permission_classes = []
    serializer_class = WorkshopSerializer

    def post(self, request: Request):
        data: Mapping = request.data
        serialzer: WorkshopSerializer = WorkshopSerializer(data=data)
        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data, status=status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
