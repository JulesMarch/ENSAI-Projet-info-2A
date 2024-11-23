
from fastapi import APIRouter, HTTPException, HTTPException, Depends, Query
from typing import List, Tuple
from src.app.auth import get_current_user
from src.app.models import User
from src.app.utils import Conversion
from src.services.fonction_1 import find_by_code_insee, find_by_nom
from src.services.fonction_2 import find_by_coord
import geopandas as gpd
import folium
from shapely.geometry import Point
from pathlib import Path
from fastapi.responses import HTMLResponse


router = APIRouter()


# Charger les données géographiques (ajuster les chemins selon tes fichiers)

script_dir = Path(__file__).resolve()

regions_shp = script_dir.parents[4] / "ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2023-05-03" / "ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2023-05-03" / "ADMIN-EXPRESS-COG" / "1_DONNEES_LIVRAISON_2023-05-03" / "ADECOG_3-2_SHP_WGS84G_FRA" / "REGION.shp"
departements_shp = script_dir.parents[4] / "ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2023-05-03" / "ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2023-05-03" / "ADMIN-EXPRESS-COG" / "1_DONNEES_LIVRAISON_2023-05-03" / "ADECOG_3-2_SHP_WGS84G_FRA" / "DEPARTEMENT.shp"
communes_shp = script_dir.parents[4] / "ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2023-05-03" / "ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2023-05-03" / "ADMIN-EXPRESS-COG" / "1_DONNEES_LIVRAISON_2023-05-03" / "ADECOG_3-2_SHP_WGS84G_FRA" / "COMMUNE.shp"


@router.get("/")
async def root():
    return {"message": "Bienvenue sur notre API ! Nous vous invitons à aller sur http://localhost:8000/docs"}


@router.post("/login")
async def login(username: str, password: str):
    print(f"Login attempt: username={username}, password={'*' * len(password)}")


@router.get("/zonageparcodesimple/{niveau}/{annee}/{code_insee}")
async def get_zone_par_code_insee_simple(
    niveau: str,
    code_insee: str,
    annee: int
):
    print(niveau, code_insee)
    answer = find_by_code_insee(str(code_insee), niveau, annee)
    return answer


@router.get("/zonageparcode/{niveau}/{annee}/{code_insee}", response_class=HTMLResponse)
async def get_zone_par_code_insee(
    niveau: str,
    code_insee: str,
    annee: int
):
    print(f"Requête reçue : Niveau={niveau}, Code INSEE={code_insee}, Année={annee}")

    # Récupérer les données avec la fonction existante
    try:
        answer = find_by_code_insee(str(code_insee), niveau, annee)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la recherche de données : {str(e)}")

    # Déterminer le fichier shapefile à utiliser en fonction du niveau
    if niveau == "Région":
        shapefile_path = regions_shp
    elif niveau == "Département":
        shapefile_path = departements_shp
    elif niveau == "Commune":
        shapefile_path = communes_shp
    else:
        raise HTTPException(status_code=400, detail=f"Niveau {niveau} non supporté. Choisissez parmi: Département, Région, Commune.")

    # Charger les données du shapefile
    try:
        gdf = gpd.read_file(shapefile_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du chargement du fichier shapefile : {str(e)}")

    # Déterminer la colonne pour le filtrage
    niveau_to_column = {
        "Département": "INSEE_DEP",
        "Région": "INSEE_REG",
        "Commune": "INSEE_COM"
    }
    column_name = niveau_to_column[niveau]

    # Filtrer les données pour trouver la zone correspondante
    highlighted_zone = gdf[gdf[column_name] == code_insee]
    if highlighted_zone.empty:
        raise HTTPException(status_code=404, detail=f"Aucune zone trouvée pour le code INSEE {code_insee} au niveau {niveau}.")

    # Centrer la carte sur la zone correspondante
    centroid = highlighted_zone.geometry.centroid.iloc[0]
    folium_map = folium.Map(location=[centroid.y, centroid.x], zoom_start=8)

    # Ajouter toutes les zones en gris clair
    folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            'fillColor': 'lightgray',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.5
        }
    ).add_to(folium_map)

    # Ajouter la zone sélectionnée en orange
    folium.GeoJson(
        highlighted_zone,
        style_function=lambda feature: {
            'fillColor': 'orange',
            'color': 'red',
            'weight': 2,
            'fillOpacity': 0.7
        },
        tooltip=folium.GeoJsonTooltip(fields=["NOM", column_name], aliases=["Nom:", "Code INSEE:"])
    ).add_to(folium_map)

    # Ajouter un marqueur pour le centroïde
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"{niveau}: {highlighted_zone['NOM'].iloc[0]} (INSEE: {code_insee})"
    ).add_to(folium_map)

    # Sauvegarder la carte dans un fichier HTML temporaire
    output_dir = Path("./temp_maps")
    output_dir.mkdir(exist_ok=True)  # Créer le dossier s'il n'existe pas
    map_path = output_dir / f"map_{niveau}_{code_insee}.html"
    try:
        folium_map.save(map_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde de la carte : {str(e)}")

    # Retourner la carte HTML comme réponse
    return map_path.read_text(encoding='utf-8')


@router.get("/zonageparnom/{niveau}/{annee}/{nom}")
async def get_zone_par_nom(
    niveau: str,
    nom: str,
    annee: int
):
    answer = find_by_nom(str(nom), niveau, annee)
    return answer


@router.get("/coordonnees_simples/{niveau}")
async def find_coord_simple(
    niveau: str,
    lat: float = Query(..., description="Latitude du point"),
    long: float = Query(..., description="Longitude du point"),
    annee: int = Query(..., description="Année de la recherche"),
    type_coord: str = "GPS"
):
    # Conversion des coordonnées si nécessaire
    orig_lat, orig_long = lat, long
    if type_coord == "Lambert":
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

    elif niveau == "Département":
        resultat_final["nom"] = answer[0].nom
        resultat_final["code_insee"] = answer[0].num_dep
        resultat_final["région"] = answer[1].nom

    elif niveau == "Commune":
        resultat_final["nom"] = answer[0].nom
        resultat_final["code_insee"] = answer[0].code_postal
        resultat_final["département"] = answer[1][0].nom
        resultat_final["région"] = answer[1][1].nom

    elif niveau == "Arrondissement":
        resultat_final["nom"] = answer[0].nom
        resultat_final["code_insee"] = answer[0].num_arr
        resultat_final["commune"] = answer[1][0].nom
        resultat_final["département"] = answer[1][1][0].nom
        resultat_final["région"] = answer[1][1][1].nom

    elif niveau == "Iris":
        resultat_final["nom"] = answer[0].nom
        resultat_final["code_insee"] = answer[0].num_iris
        resultat_final["commune"] = answer[1][0].nom
        resultat_final["département"] = answer[1][1][0].nom
        resultat_final["région"] = answer[1][1][1].nom

    return resultat_final


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
        resultat_final["département"] = answer[1][0].nom
        resultat_final["région"] = answer[1][1].nom

    elif niveau == "Arrondissement":
        resultat_final["nom"] = answer[0].nom
        resultat_final["code_insee"] = answer[0].num_arr
        resultat_final["commune"] = answer[1][0].nom
        resultat_final["département"] = answer[1][1][0].nom
        resultat_final["région"] = answer[1][1][1].nom

    elif niveau == "Iris":
        resultat_final["nom"] = answer[0].nom
        resultat_final["code_insee"] = answer[0].num_iris
        resultat_final["commune"] = answer[1][0].nom
        resultat_final["département"] = answer[1][1][0].nom
        resultat_final["région"] = answer[1][1][1].nom

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


@router.post("/listepoints/")
async def find_points_loc(
    points: List[Tuple[float, float, str]],
    #vcurrent_user: User = Depends(get_current_user)  # Protection par authentification
):
    # print(f"Utilisateur authentifié : {current_user.username}")
    dic_retour = {}
    for i, point in enumerate(points):
        try:
            answer = find_by_coord(float(point[1]), float(point[0]), point[2])
            niveau = point[2]
            resultat_final = {
                "coordonées": (float(point[0]), float(point[1])),
                "niveau": niveau,
            }
            if niveau == "Région":
                resultat_final["nom"] = answer.nom
                resultat_final["code_insee"] = answer.num_rgn

            elif niveau == "Département":
                resultat_final["nom"] = answer[0].nom
                resultat_final["code_insee"] = answer[0].num_dep
                resultat_final["région"] = answer[1].nom

            elif niveau == "Commune":
                resultat_final["nom"] = answer[0].nom
                resultat_final["code_insee"] = answer[0].code_postal
                resultat_final["département"] = answer[1][0].nom
                resultat_final["région"] = answer[1][1].nom

            elif niveau == "Arrondissement":
                resultat_final["nom"] = answer[0].nom
                resultat_final["code_insee"] = answer[0].num_arr
                resultat_final["commune"] = answer[1][0].nom
                resultat_final["département"] = answer[1][1][0].nom
                resultat_final["région"] = answer[1][1][1].nom

            elif niveau == "Iris":
                resultat_final["nom"] = answer[0].nom
                resultat_final["code_insee"] = answer[0].num_iris
                resultat_final["commune"] = answer[1][0].nom
                resultat_final["département"] = answer[1][1][0].nom
                resultat_final["région"] = answer[1][1][1].nom

            dic_retour[f"Point {i + 1}"] = resultat_final
        except Exception as e:
            dic_retour[f"Point {i + 1}"] = {"error": "Point introuvable", "detail": str(e)}
    return dic_retour
