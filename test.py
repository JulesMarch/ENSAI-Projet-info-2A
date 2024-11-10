from src.dao.point_dao import PointDao, Point
from src.dao.polygone_dao import PolygoneDao

test = PointDao()

p = Point(0.1, 0.4)

PointDao.add_point((p.x, p.y))
PointDao.add_point((p.x, p.y))

PointDao.add_point((2, 3))
PointDao.add_point((2, 3))

PointDao.add_point((1, 0))
