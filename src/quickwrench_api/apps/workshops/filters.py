import django_filters
from .models import Workshop


class WorkshopFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields=(
            ("account__username", "account__username"),
            ("name", "name"),
            ("address", "address"),
            ("services__name", "services__name"),
        ),
        field_labels={
            "account__username": "exitinguser",
            "name": "bimmerfixes",
            "address": "zayed",
            "service__name": "Oil",
        },
    )

    class Meta:
        model = Workshop
        fields = {
            "account__username": ["icontains"],
            "account__phone_number": ["icontains"],
            "name": ["icontains"],
            "address": ["icontains"],
            "services__name": ["icontains"],
            "services__price": ["exact", "lte", "gte"],
        }
