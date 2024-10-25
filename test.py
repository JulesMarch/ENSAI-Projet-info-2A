from src.dao.point_dao import PointDao, Point
from src.dao.db_connection import DBConnection

test = PointDao()

p = Point(0,0)

PointDao.add_point((p.x,p.y))
PointDao.add_point((p.x,p.y))


