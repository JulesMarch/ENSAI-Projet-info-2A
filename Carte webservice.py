import geopandas as gpd
import folium
from shapely.geometry import Point
from fastapi import APIRouter, Query

router = APIRouter()

# Charger les données géographiques (ajuster les chemins selon tes fichiers)
regions_shp = "path/to/regions.shp"
departements_shp = "path/to/departements.shp"
communes_shp = "path/to/communes.shp"

# Définir la fonction
@router.get("/coordonees/{niveau}")
async def find_coord(
    niveau: str,
    lat: float = Query(..., description="Latitude du point"),
    long: float = Query(..., description="Longitude du point"),
    annee: int = Query(..., description="Année de la recherche"),
    type_coord: str = "GPS"
):
    # Conversion des coordonnées si nécessaire
    orig_lat, orig_long = lat, long
    if type_coord == "Lambert":
        orig_lat, orig_long = lat, long
        long, lat = Conversion.lambert93_into_gps(long, lat)
        print(long, lat)

    # Trouver la zone correspondant aux coordonnées
    answer = find_by_coord(long, lat, niveau)
    resultat_final = {
        "coordonées": (orig_lat, orig_long),
        "niveau": niveau,
    }

    # Ajouter les informations spécifiques à chaque niveau
    if niveau == "Région":
        resultat_final["nom"] = answer.nom
        resultat_final["code_insee"] = answer.num_rgn
        shapefile_path = regions_shp

    elif niveau == "Département":
        resultat_final["nom"] = answer[0].nom
        resultat_final["code_insee"] = answer[0].num_dep
        resultat_final["région"] = answer[1].nom
        shapefile_path = departements_shp

    elif niveau == "Commune":
        resultat_final["nom"] = answer[0].nom
        resultat_final["code_insee"] = answer[0].code_postal
        resultat_final["département"] = answer[1].nom
        shapefile_path = communes_shp

    else:
        return {"error": "Niveau non pris en charge"}

    # Charger le shapefile correspondant
    gdf = gpd.read_file(shapefile_path)

    # Créer un objet Point pour les coordonnées
    point = Point(long, lat)

    # Trouver la zone géographique qui contient le point
    zone_contenant = gdf[gdf.contains(point)]
    if zone_contenant.empty:
        return {"error": "Aucune zone trouvée pour ces coordonnées"}

    # Créer une carte interactive
    nom_zone = zone_contenant.iloc[0]["NOM"]  # Ajuster selon le champ contenant le nom
    m = folium.Map(location=[lat, long], zoom_start=8)

    # Ajouter le point sur la carte
    folium.Marker(
        location=[lat, long],
        popup=f"Point ({lat}, {long})",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

    # Ajouter les polygones avec la zone surlignée
    def style_function(feature):
        if feature["properties"]["NOM"] == nom_zone:
            return {"fillColor": "red", "color": "black", "weight": 2, "fillOpacity": 0.7}
        else:
            return {"fillColor": "lightgray", "color": "black", "weight": 1, "fillOpacity": 0.5}

    folium.GeoJson(
        data=gdf,
        name="Zones géographiques",
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=["NOM"])
    ).add_to(m)

    # Sauvegarder la carte en tant que fichier HTML
    output_path = f"carte_interactive_{niveau}.html"
    m.save(output_path)
    print(f"Carte sauvegardée sous {output_path}.")

    # Retourner les résultats et le chemin de la carte
    resultat_final["carte"] = output_path
    return resultat_final
