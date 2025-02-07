from typing import Optional
from uuid import UUID

from ninja import ModelSchema

from main.apps.users.models import User


class UserDetailSchema(ModelSchema):
    id: UUID
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: str

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
        ]
