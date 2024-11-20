import geopandas as gpd
import folium

# Chemin vers ton fichier shapefile
shapefile_path = "Departementfr/DEPARTEMENT.shp"

# Charger le fichier shapefile
gdf = gpd.read_file(shapefile_path)

# Afficher les premières lignes pour vérifier le contenu
print(gdf.head())

# Fonction pour styliser la carte avec un département spécifique mis en surbrillance
def create_map_with_highlight(departement_cible):
    def style_function(feature):
        # Applique le style rouge uniquement au département ciblé
        if feature['properties']['NOM_M'] == departement_cible:
            return {'fillColor': 'red', 'color': 'black', 'weight': 2, 'fillOpacity': 0.7}
        else:
            return {'fillColor': 'lightblue', 'color': 'black', 'weight': 1, 'fillOpacity': 0.5}

    # Créer une carte centrée sur la France
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=5)

    # Ajouter les polygones des départements avec le style personnalisé
    folium.GeoJson(
        data=gdf,
        name="Départements de France",
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=['NOM_M'])  # Affiche le nom du département au survol
    ).add_to(m)

    # Sauvegarder la carte en tant que fichier HTML
    output_path = f"carte_departements_{departement_cible}.html"
    m.save(output_path)
    print(f"Carte avec le département {departement_cible} mis en évidence sauvegardée sous {output_path}.")

# Appeler la fonction avec le département souhaité
create_map_with_highlight("ILLE-ET-VILAINE")  # Remplace "Paris" par le nom du département que tu veux mettre en surbrillance





