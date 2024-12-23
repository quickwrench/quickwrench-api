import pytest

from quickwrench_api.apps.accounts.models import Account
from quickwrench_api.apps.car_makes.models import CarMake
from quickwrench_api.apps.workshops.models import Service, Category, Workshop


@pytest.fixture
def test_service(db, load_data) -> Service:
    category: Category = Category.objects.get(id=1)
    return Service.objects.create(
        category=category,
        name="Oil",
        description="description",
        price=99,
    )


@pytest.fixture
def workshop_data(test_account: dict[str, str], test_service: Service):
    return {
        "account": test_account,
        "carmakes": [1],
        "services": [
            {
                "name": test_service.name,
                "description": test_service.description,
                "category": test_service.category.id,
                "price": test_service.price,
            }
        ],
        "name": "bimmerfixes",
        "address": "zayed",
    }


@pytest.fixture
def existing_workshop() -> dict:
    return {
        "account": {
            "email": "existinguser@example.com",
            "username": "existinguser",
            "password": "testpass",
            "phone_number": "+201101234567",
        },
        "name": "bimmerfixes",
        "address": "zayed",
    }


@pytest.fixture
def workshop_with_existing_email(
    db,
    test_service: Service,
    existing_workshop: dict,
    load_data,
) -> Workshop:
    carmakes = CarMake.objects.get(id=1)
    account: dict[str, str] = Account.objects.create_user(
        email=existing_workshop["account"]["email"],
        username=existing_workshop["account"]["username"],
        password=existing_workshop["account"]["password"],
        phone_number=existing_workshop["account"]["phone_number"],
    )
    workshop: Workshop = Workshop.objects.create(
        account=account,
        name=existing_workshop["name"],
        address=existing_workshop["address"],
    )
    workshop.services.set([test_service])
    workshop.carmakes.set([carmakes])
    return workshop
