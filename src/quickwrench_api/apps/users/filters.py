import django_filters
from .models import User


class UserFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields=(
            ("account__username", "account__username"),
            ("first_name", "first_name"),
            ("last_name", "last_name"),
        ),
        field_labels={
            "account__username": "Username",
            "first_name": "First_name",
            "last_name": "Last_name",
        },
    )

    class Meta:
        model = User
        fields = {
            "account__username": ["icontains"],
            "account__phone_number": ["icontains"],
            "first_name": ["icontains"],
            "last_name": ["icontains"],
        }
