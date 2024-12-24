import pytest

from quickwrench_api.apps.carmakes.models import CarMake
from quickwrench_api.apps.users.models import User
from quickwrench_api.apps.workshops.models import Workshop


@pytest.fixture
def authenticated_workshop(load_data, authenticated_account, test_service):
    carmakes = CarMake.objects.get(id=1)
    workshop = Workshop.objects.create(account=authenticated_account, address="october")
    workshop.services.set([test_service])
    workshop.carmakes.set([carmakes])
    return workshop


@pytest.fixture
def authenticated_user(authenticated_account, load_data):
    carmake = CarMake.objects.get(id=1)
    user = User.objects.create(
        account=authenticated_account,
        first_name="first",
        last_name="last",
        carmake=carmake,
    )
    return user
