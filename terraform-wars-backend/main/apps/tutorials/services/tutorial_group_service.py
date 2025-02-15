import logging
from typing import Iterable

from main.apps.tutorials.models import TutorialGroup
from main.apps.tutorials.repositories import TutorialGroupRepository


logger = logging.getLogger(__name__)


class TutorialGroupService:
    def __init__(self, tutorial_group_repository: TutorialGroupRepository):
        self.tutorial_group_repository = tutorial_group_repository

    def get_tutorial_groups(self) -> Iterable[TutorialGroup]:
        return self.tutorial_group_repository.get_all()
