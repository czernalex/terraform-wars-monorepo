from typing import Optional
from uuid import UUID

from ninja import ModelSchema, FilterSchema, Schema

from main.apps.tutorials.enums import TutorialGroupState
from main.apps.tutorials.models import TutorialGroup


class GetTutorialGroupFilterSchema(FilterSchema):
    user_id: Optional[UUID] = None
    state: Optional[TutorialGroupState] = None


class CreateTutorialGroupSchema(Schema):
    title: str
    description: str


class UpdateTutorialGroupSchema(Schema):
    title: str
    description: str


class TutorialGroupListSchema(ModelSchema):
    id: UUID
    state: TutorialGroupState
    tutorial_count: int

    class Meta:
        model = TutorialGroup
        fields = ("id", "title", "description", "state")


class TutorialGroupDetailSchema(ModelSchema):
    id: UUID
    state: TutorialGroupState

    class Meta:
        model = TutorialGroup
        fields = ("id", "title", "description", "state")
