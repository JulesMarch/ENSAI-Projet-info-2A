import src.dao.point_dao
import pytest


class TestPointDao:
    def test_add_point(self):
        # GIVEN
        attack_dao = AttackDao()

        # WHEN
        attacks = attack_dao.find_all_attacks(100)

        # THEN
        assert len(attacks) == 100