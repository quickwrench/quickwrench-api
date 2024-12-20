import pytest
from quickwrench_api.apps.accounts.models import Account
from quickwrench_api.apps.workshops.models import Workshop
from quickwrench_api.apps.car_makes.models import CarMake
from quickwrench_api.apps.users.models import User


@pytest.fixture
def authenticated_workshop(load_data, authenticated_account, test_service):
    car_makes = CarMake.objects.get(id=1)
    workshop = Workshop.objects.create(account=authenticated_account, address="october")
    workshop.services.set([test_service])
    workshop.carmakes.set([car_makes])
    return workshop


@pytest.fixture
def authenticated_user(authenticated_account, load_data):
    car_make = CarMake.objects.get(id=1)
    user = User.objects.create(
        account=authenticated_account,
        first_name="first",
        last_name="last",
        car_make=car_make,
    )
    return user
