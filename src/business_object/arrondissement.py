from src.business_object.zonage import Zonage
from src.business_object.segment import Segment


class Arrondissement(Zonage):
    def __init__(
        self,
        num_arr: int,
        nom: str,
        perimetre: list[Segment],
        creux,
        edition_carte: int
    ):
        super().__init__(nom, perimetre, creux, edition_carte)
        self.num_arr = num_arr
