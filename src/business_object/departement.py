from src.business_object.zonage import Zonage
from src.business_object.segment import Segment


class Departement(Zonage):
    def __init__(
        self,
        num_dep: int,
        nom: str,
        perimetre: list[Segment],
        creux,
        edition_carte: int
    ):
        super().__init__(nom, perimetre, creux, edition_carte)
        self.num_dep = num_dep
