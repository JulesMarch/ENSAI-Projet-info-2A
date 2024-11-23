import src.services.fonction_1 as F1


class TestFonction1():
    def test_find_by_code_insee(self, request):

        # WHEN

        # Pour les Régions
        resultat_1 = F1.find_by_code_insee(
            code_insee='75', niveau='Région', annee=2023
        )
        resultat_2 = F1.find_by_code_insee(
            code_insee='44', niveau='Région', annee=2023
        )

        # Pour les Départements
        resultat_3 = F1.find_by_code_insee(
            code_insee='35', niveau='Département', annee=2023
        )
        resultat_4 = F1.find_by_code_insee(
            code_insee='09', niveau='Département', annee=2023
        )

        # Pour les Communes
        resultat_5 = F1.find_by_code_insee(
            code_insee=75056, niveau='Commune', annee=2023
        )
        resultat_6 = F1.find_by_code_insee(
            code_insee=35238, niveau='Commune', annee=2023
        )

        # THEN
        assert resultat_1 == request.getfixturevalue(
            "Region_Nouvelle_Aquitaine_kwargs"
        )
        assert resultat_2 == request.getfixturevalue(
            "Region_Grand_Est_kwargs"
        )

        assert resultat_3 == request.getfixturevalue(
            "Departement_Ille_et_Villaine_kwargs"
        )
        assert resultat_4 == request.getfixturevalue(
            "Departement_Ariege_kwargs"
        )

        assert resultat_5 == request.getfixturevalue("Commune_Paris_kwargs")
        assert resultat_6 == request.getfixturevalue("Commune_Rennes_kwargs")

    def test_find_by_nom(self, request):

        # WHEN

        # Pour les Régions
        resultat_1 = F1.find_by_nom(
            nom='Nouvelle-Aquitaine', niveau='Région', annee=2023
        )
        resultat_2 = F1.find_by_nom(
            nom='GranD esT', niveau='Région', annee=2023
        )

        # Pour les Départements
        resultat_3 = F1.find_by_nom(
            nom='Ille-et-Vilaine', niveau='Département', annee=2023
        )
        resultat_4 = F1.find_by_nom(
            nom='aRiEge', niveau='Département', annee=2023
        )

        # Pour les Communes
        resultat_5 = F1.find_by_nom(
            nom='Paris', niveau='Commune', annee=2023
        )
        resultat_6 = F1.find_by_nom(
            nom='REnnes', niveau='Commune', annee=2023
        )

        # THEN
        assert resultat_1 == request.getfixturevalue(
            "Region_Nouvelle_Aquitaine_kwargs"
        )
        assert resultat_2 == request.getfixturevalue(
            "Region_Grand_Est_kwargs"
        )

        assert resultat_3 == request.getfixturevalue(
            "Departement_Ille_et_Villaine_kwargs"
        )
        assert resultat_4 == request.getfixturevalue(
            "Departement_Ariege_kwargs"
        )

        assert resultat_5 == request.getfixturevalue("Commune_Paris_kwargs")
        assert resultat_6 == request.getfixturevalue("Commune_Rennes_kwargs")
