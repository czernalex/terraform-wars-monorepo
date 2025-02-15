import abc
from typing import Iterable

from main.apps.tutorials.models.tutorial_group import TutorialGroup


class TutorialGroupRepository(abc.ABC):
    @abc.abstractmethod
    def get_all(self) -> Iterable[TutorialGroup]:
        pass


class DjangoORMTutorialGroupRepository(TutorialGroupRepository):
    def get_all(self) -> Iterable[TutorialGroup]:
        return TutorialGroup.objects.all()
