from src.business_object.zonage import Zonage
from src.business_object.segment import Segment


class Region(Zonage):
    def __init__(
        self,
        num_rgn: int,
        nom: str,
        perimetre: list[Segment],
        creux,
        edition_carte: int):
        super().__init__(nom, perimetre, creux, edition_carte)  # Appel du constructeur de Zonage
        self.num_rgn = num_rgn
