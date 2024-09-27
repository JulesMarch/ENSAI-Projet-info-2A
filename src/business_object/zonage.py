from abc import ABC


class Zonage(ABC):
    def __init__(self, nom: str, coord: list, edition_carte: int):
        self.nom = nom
        self.coord = coord
        self.edition_carte = edition_carte
