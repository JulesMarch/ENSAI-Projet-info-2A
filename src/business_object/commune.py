from zonage import Zonage


class Commune(Zonage):
    def __init__(self, code_postal: int):
        self.code_postal = code_postal
