from typing import Mapping

from rest_framework import status, generics
from django_filters import rest_framework as filters
from .filters import WorkshopFilter

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Workshop

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


class WorkshopDetailsAPIView(APIView):
    permission_classes = []
    serializer_class = WorkshopSerializer

    def get(self, request, id):
        workshop = Workshop.objects.filter(account=id).first()
        if workshop:
            serializer = self.serializer_class(workshop)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"message": "Workshop does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
<<<<<<< HEAD

=======
>>>>>>> 29eb026232c4fe274c7afb7b5c9205c0cfc9d643

class WorkshopListView(generics.ListAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = []
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = WorkshopFilter
<<<<<<< HEAD
=======

>>>>>>> 29eb026232c4fe274c7afb7b5c9205c0cfc9d643
