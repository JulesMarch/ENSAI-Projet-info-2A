class Utilisateur:
    def __init_(self, nom: str, adresse_mail: str, mdp: str):
        self.nom = nom
        self.adresse_mail = adresse_mail
        self.__mdp = mdp
