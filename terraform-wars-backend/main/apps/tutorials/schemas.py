from uuid import UUID

from ninja import ModelSchema

from main.apps.tutorials.enums import TutorialGroupState
from main.apps.tutorials.models import TutorialGroup


class TutorialGroupListSchema(ModelSchema):
    id: UUID
    state: TutorialGroupState

    class Meta:
        model = TutorialGroup
        fields = ("id", "title", "description", "state")
