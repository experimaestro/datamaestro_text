from experimaestro import Param
from datamaestro.data import Base, File
import datamaestro.data.csv as csv


class RatedItems(Base):
    ratings: Param[File]


class Movielens(RatedItems):
    links: Param[csv.Generic]
    movies: Param[csv.Generic]
    tags: Param[csv.Generic]
