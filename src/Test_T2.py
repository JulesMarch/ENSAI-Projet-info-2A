import os
import geopandas as gpd
from bs4 import BeautifulSoup
from main import create_map_with_highlight  # Remplace `main` par le nom de ton fichier contenant la fonction

# Charger les données nécessaires pour le test
shapefile_path = "Departementfr/DEPARTEMENT.shp"
gdf = gpd.read_file(shapefile_path)

# Vérifie qu'au moins un département est disponible pour les tests
def test_shapefile_data():
    assert not gdf.empty, "Le shapefile est vide."
    assert 'NOM' in gdf.columns, "La colonne 'NOM' est absente du shapefile."

# Teste la création de la carte avec un département spécifique
def test_create_map_with_highlight():
    departement_test = "Paris"  # Nom d'un département à tester (doit exister dans le shapefile)
    output_file = f"carte_departements_{departement_test}.html"

    # Supprime le fichier si existant avant le test
    if os.path.exists(output_file):
        os.remove(output_file)

    # Appelle la fonction pour créer la carte
    create_map_with_highlight(departement_test)

    # Vérifie que le fichier HTML est généré
    assert os.path.exists(output_file), f"Le fichier {output_file} n'a pas été généré."

    # Analyse le contenu du fichier avec BeautifulSoup pour valider le département
    with open(output_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        assert departement_test in soup.text, f"Le département {departement_test} n'est pas mis en surbrillance."

    # Supprime le fichier généré après le test
    os.remove(output_file)

# Teste la fonction avec un département inexistant
def test_create_map_with_nonexistent_departement():
    departement_inexistant = "Atlantis"
    output_file = f"carte_departements_{departement_inexistant}.html"

    # Supprime le fichier si existant avant le test
    if os.path.exists(output_file):
        os.remove(output_file)

    # Appelle la fonction pour créer la carte
    create_map_with_highlight(departement_inexistant)

    # Vérifie que le fichier HTML est généré
    assert os.path.exists(output_file), f"Le fichier {output_file} n'a pas été généré."

    # Analyse le contenu du fichier pour vérifier que le département n'est pas présent
    with open(output_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        assert departement_inexistant not in soup.text, f"Un département inexistant ({departement_inexistant}) ne devrait pas apparaître."

    # Supprime le fichier généré après le test
    os.remove(output_file)
