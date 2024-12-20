from rest_framework.views import APIView
from rest_framework import status
from .serializers import AccountSerializer
from rest_framework.permissions import IsAuthenticated
from ..users.models import User
from ..workshops.models import Workshop
from rest_framework.response import Response


class AccountDetailsAPIView(APIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        user = User.objects.filter(account=current_user).first()
        workshop = Workshop.objects.filter(account=current_user).first()
        if user:
            account_type = "user"
            serializer = self.serializer_class(user.account)
        elif workshop:
            account_type = "workshop"
            serializer = self.serializer_class(workshop.account)
        else:
            return Response(
                {"message": "No associated user or workshop found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        response_data = serializer.data
        response_data["type"] = account_type
        return Response(response_data, status=status.HTTP_200_OK)
