from abc import ABC
from src.business_object.segment import Segment


class Zonage(ABC):
    def __init__(
        self,
        nom: str,
        perimetre: list(Segment),
        creux: list(Segment),
        edition_carte: int
    ):

        self.nom = nom
        self.perimetre = perimetre
        self.creux = creux
        self.edition_carte = edition_carte
