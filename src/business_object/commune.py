from src.business_object.zonage import Zonage
from src.business_object.segment import Segment

class Commune(Zonage):
    def __init__(
        self,
        code_postal: int,
        nom: str,
        perimetre: list[Segment],
        creux,
        edition_carte: int):
        super().__init__(nom, perimetre, creux, edition_carte)  # Appel du constructeur de Zonage
        self.code_postal = code_postal
