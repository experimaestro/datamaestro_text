from datamaestro.data import Base, File, argument
import datamaestro.data.csv as csv


@argument("ratings", type=File)
class RatedItems(Base):
    pass


@argument("links", type=csv.Generic)
@argument("movies", type=csv.Generic)
@argument("tags", type=csv.Generic)
class Movielens(RatedItems):
    pass
