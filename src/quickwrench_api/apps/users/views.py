from typing import Mapping
from .models import User

from rest_framework import status, generics


from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from django_filters import rest_framework as filters
from .filters import UserFilter



class RegisterAPIView(APIView):
    permission_classes = []
    serializer_class = UserSerializer

    def post(self, request: Request):
        data: Mapping = request.data
        serializer: UserSerializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsAPIView(APIView):
    permission_classes = []
    serializer_class = UserSerializer

    def get(self, request, id):
        user = User.objects.filter(account=id).first()
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )



class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter

