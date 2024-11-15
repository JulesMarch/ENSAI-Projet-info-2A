import fiona

with fiona.open(
    "//filer-eleves2/id2505/Cours2A/"
    "ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2023-05-03/"
    "ADMIN-EXPRESS-COG_3-2__SHP_WGS84G_FRA_2023-05-03/"
    "ADMIN-EXPRESS-COG/1_DONNEES_LIVRAISON_2023-05-03/"
    "ADECOG_3-2_SHP_WGS84G_FRA/REGION.shp",
    'r'
) as shapefile:

    for region in shapefile:
        properties = region["properties"]
        geometry = region["geometry"]

        type_comp = geometry["type"]

        if type_comp == 'Polygon':

            polygon = geometry["coordinates"][0]

            # print(len(polygon))

        elif type_comp == 'MultiPolygon':

            print(geometry)

            list_polygon = geometry["coordinates"]

            print(len(list_polygon), type(list_polygon))

            polygon = list_polygon[0]

            print(len(polygon), type(polygon))

            list_point = list_polygon[0][0]

            print(len(list_point), type(list_point))

            point = list_polygon[0][0][0]

            print(len(point), type(point))
