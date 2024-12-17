import pytest
from quickwrench_api.apps.users.models import User
from quickwrench_api.apps.accounts.models import Account
from quickwrench_api.apps.car_makes.models import CarMake


@pytest.fixture()
def user_to_fetch(db, load_carmake_data) -> User:
    car_make: CarMake = CarMake.objects.get(id=1)
    account: Account = Account.objects.create_user(
        email="testuser@test.com", username="username123", password="testpass"
    )
    user: User = User.objects.create(
        account=account, first_name="first", last_name="last", car_make=car_make
    )
    return user
