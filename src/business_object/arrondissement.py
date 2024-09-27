from zonage import Zonage
from commune import Commune


class Arrondissement(Zonage):
    def __init__(self, num_arr: int, ville_associee: Commune):
        self.num_arr = num_arr
        self.ville_associee = ville_associee
