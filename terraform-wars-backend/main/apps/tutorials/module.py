import anydi

from main.apps.tutorials.repositories import DjangoORMTutorialGroupRepository, TutorialGroupRepository
from main.apps.tutorials.services import TutorialGroupService


class TutorialsModule(anydi.Module):
    @anydi.provider(scope="singleton")
    def tutorial_group_repository(self) -> TutorialGroupRepository:
        return DjangoORMTutorialGroupRepository()

    @anydi.provider(scope="singleton")
    def tutorial_group_service(self, tutorial_group_repository: TutorialGroupRepository) -> TutorialGroupService:
        return TutorialGroupService(tutorial_group_repository=tutorial_group_repository)
