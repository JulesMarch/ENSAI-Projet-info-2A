from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection

from src.business_object.point import Point
from src.business_object.zonage import Zonage
from src.dao.contour_dao import ContourDao


niveaux = ["Région", "Département", "Commune", "Arrondissement", "IRIS"]


class ZonageDao(metaclass=Singleton):
    def add_zone_geo(zone: dict):
        """
        Ajoute une zone géographique à la base de données 
        si elle n'est pas déjà présente

        Args:
            zone (dict): Dictionnaire contenant les informations de la zone, 
            telles que le nom, le niveau et le code.
        """

        # if not ZonageDao.est_dans(zone):

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DO $$                                              "
                    "BEGIN                                              "
                    "   IF NOT EXISTS (SELECT 1 FROM pg_class           "
                    "WHERE relname = 'seq_id_zone_geo') THEN"
                    "   EXECUTE 'CREATE SEQUENCE seq_id_zone_geo';      "
                    "   END IF;                                         "
                    "END $$;                                            "

                    "INSERT INTO projet.zone_geo (id_zone, nom, niveau, "
                    " code_insee, niveau_superieur) VALUES              "
                    " (nextval('seq_id_zone_geo'), %(nom)s, %(niveau)s, "
                    " %(code_insee)s, %(niveau_superieur)s)             ",
                    {
                        "nom": zone["NOM"],
                        "niveau": "Région",
                        "code_insee": zone["INSEE_REG"],
                        "niveau_superieur": "Null"
                    },
                )

    def est_dans(zone: dict) -> bool:
        """
        Vérifie si une zone géographique est présente dans la base de données

        Args:
            zone (dict): Dictionnaire contenant les informations de la zone, 
            telles que le nom, le niveau, et le code INSEE

        Returns:
            bool: Retourne True si la zone est dans la base de données, 
            False sinon
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from projet.point                          "
                    "   where nom, niveau, code_insee                    ",
                    {
                        "nom": zone["NOM"]
                    },
                )
                res = cursor.fetchone()

        if res:

            return True

        return False

    def construction_zonage(zone):
        """
        Construit un objet Zonage à partir des données d'une zone géographique
    
        Args:
            zone (dict): Informations sur la zone géographique, avec au minimum
            le champ 'code_insee' pour l'identification
                     
        Returns:
            Zonage: Objet représentant la zone avec ses contours (périmètre et creux)
        """
        
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT x, y, creux, id_polygone FROM projet.point "
                    "JOIN projet.association_polygone_point USING (id_point) "
                    "JOIN projet.polygone USING (id_polygone) "
                    "JOIN projet.association_connexe_polygone USING"
                    "(id_polygone)"
                    "JOIN projet.comp_connexe USING (id_comp_connexe)"
                    "JOIN projet.asso_zone_comp_co USING (id_comp_connexe)"
                    "JOIN projet.zone_geo USING (id_zone) "
                    "where projet.zone_geo.code_insee =%(code_insee)s"
                    "ORDER BY projet.association_polygone_point.ordre ASC",
                    {
                        "code_insee": zone["code_insee"]
                    }
                )
                pts_perim = cursor.fetchall()

            print(zone["nom"])
            print("total : ", len(pts_perim))
            lst_pts_perim = []
            lst_poly_perim_id = []
            lst_pts_creux = []
            lst_poly_creux_id = []
            for pt in pts_perim:
                if not pt["creux"]:
                    # print(pt["creux"])
                    lst_pts_perim.append([Point(pt["x"], pt["y"]),
                                         pt["id_polygone"]])
                    if pt["id_polygone"] not in lst_poly_perim_id:
                        lst_poly_perim_id.append(pt["id_polygone"])
                else:
                    # print(pt["id_polygone"])
                    lst_pts_creux.append([Point(pt["x"], pt["y"]),
                                         pt["id_polygone"]])
                    if pt["id_polygone"] not in lst_poly_creux_id:
                        lst_poly_creux_id.append(pt["id_polygone"])
            print("sans creux : ", len(lst_pts_perim))
            print("creux : ", len(lst_pts_creux))

            print("Etape 1 réussie")

            points_perim_dict = {}
            for point in lst_pts_perim:
                # point[1] est la clé, et on stocke toutes les valeurs
                # associées dans une liste
                if point[1] not in points_perim_dict:
                    points_perim_dict[point[1]] = []
                points_perim_dict[point[1]].append(point[0])

            # Construire lst_poly_perim
            lst_poly_perim = []
            for i in lst_poly_perim_id:
                # Récupérer les points correspondant directement
                # depuis le dictionnaire
                temp_lst = points_perim_dict.get(i, [])
                if temp_lst:
                    lst_poly_perim.append(temp_lst)

            points_creux_dict = {}
            for point in lst_pts_creux:
                # point[1] est la clé, et on stocke toutes les valeurs
                # associées dans une liste
                if point[1] not in points_creux_dict:
                    points_creux_dict[point[1]] = []
                points_creux_dict[point[1]].append(point[0])

            # Construire lst_poly_perim
            lst_poly_creux = []
            for i in lst_poly_creux_id:
                # Récupérer les points correspondant directement
                # depuis le dictionnaire
                temp_lst = points_creux_dict.get(i, [])
                if temp_lst:
                    lst_poly_creux.append(temp_lst)

            print("Etape 2 réussie")

            lst_contours_perim = []
            for poly in lst_poly_perim:
                if len(poly) > 0:
                    temp_cont = ContourDao.construction_contour(poly)
                    lst_contours_perim.append(temp_cont)

            lst_contours_creux = []
            for poly in lst_poly_creux:
                if len(poly) > 0:
                    temp_cont = ContourDao.construction_contour(poly)
                    lst_contours_creux.append(temp_cont)

            print("Etape 3 réussie")

        zone = Zonage(
            nom=zone["nom"],
            perimetre=lst_contours_perim,
            creux=lst_contours_creux,
            edition_carte="2024"
        )

        return zone
