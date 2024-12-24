from typing import Optional

from ..users.models import User
from ..workshops.models import Workshop
from .models import Account


def account_type(account: Account) -> Optional[type[User | Workshop]]:
    if User.objects.filter(account=account).exists():
        return User
    if Workshop.objects.filter(account=account).exists():
        return Workshop
    return None
