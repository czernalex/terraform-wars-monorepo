from uuid import UUID

from ninja import ModelSchema

from main.apps.tutorials.models import TutorialGroup


class TutorialGroupListSchema(ModelSchema):
    id: UUID

    class Meta:
        model = TutorialGroup
        fields = ("id",)
