from typing import List
from utils.singleton import Singleton

from dao.db_connection import DBConnection
from dao.attack_dao import AttackDao

from business_object.pokemon.pokemon_factory import PokemonFactory
from business_object.pokemon.abstract_pokemon import AbstractPokemon


class RegionDao(metaclass=Singleton):
    def find_by_code(self, niveau: str, code: int):
        request = (
            f"SELECT *                                                               "
            f"  FROM tp.pokemon p                                                    "
            f"  JOIN tp.pokemon_type pt ON pt.id_pokemon_type = p.id_pokemon_type    "
            f" LIMIT {max(limit, 0)}                                                 "
            f"OFFSET {max(offset, 0)}                                                "
        )

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(request)
                res = cursor.fetchall()

        pokemons = []
        pkmn_factory = PokemonFactory()

        for row in res:
            pokemon = pkmn_factory.instantiate_pokemon(
                type=row["pokemon_type_name"],
                hp=row["hp"],
                attack=row["attack"],
                defense=row["defense"],
                sp_atk=row["spe_atk"],
                sp_def=row["spe_def"],
                speed=row["speed"],
                level=row["level"],
                name=row["name"],
            )
            pokemons.append(pokemon)
        return pokemons