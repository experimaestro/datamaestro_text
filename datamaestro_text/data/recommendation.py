from pathlib import Path
from datamaestro.data import Base, File, argument, data
import datamaestro.data.csv as csv


@argument("ratings", type=File)
@data()
class RatedItems(Base):
    pass


@argument("links", type=csv.Generic)
@argument("movies", type=csv.Generic)
@argument("tags", type=csv.Generic)
@data()
class Movielens(RatedItems):
    pass
