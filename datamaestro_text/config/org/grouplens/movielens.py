# tasks:
#   - Recommendation
#   - Collaborative Filtering

# download:
#   handler: /archive:Zip
#   url: http://files.grouplens.org/datasets/movielens/ml-20m.zip
#   size: 190M
#   checksum: cd245b17a1ae2cc31bb14903e1204af3
# ...
# ---
# id: tmdb
# description: TMDB (The Movie database) download for MovieLens movies
# download:
#   handler: tmdb:MovieLens


from datamaestro.definitions import dataset
from datamaestro.download.archive import zipdownloader
import datamaestro.data.csv as csv
from datamaestro_text.data.recommendation import Movielens


@zipdownloader(
    "ds", "http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
)
@dataset(url="https://grouplens.org/datasets/movielens/latest/", timestamp=True)
def small(ds) -> Movielens:
    """MovieLens (small dataset)

  100,000 ratings and 3,600 tag applications applied to 9,000 movies by 600 users (as of 9/2018)
  """
    return {
        "ratings": csv.Generic(path=ds / "ratings.csv", names_row=0),
        "links": csv.Generic(path=ds / "links.csv", names_row=0),
        "movies": csv.Generic(path=ds / "movies.csv", names_row=0),
        "tags": csv.Generic(path=ds / "tags.csv", names_row=0),
    }


@zipdownloader("ds", "http://files.grouplens.org/datasets/movielens/ml-latest.zip")
@dataset(url="https://grouplens.org/datasets/movielens/latest/", timestamp=True)
def full(ds) -> Movielens:
    """MovieLens (full dataset)

  27,000,000 ratings and 1,100,000 tag applications applied to 58,000 movies by 280,000 users (as of 9/2018)
  """
    return {
        "ratings": csv.Generic(path=ds / "ratings.csv", names_row=0),
        "links": csv.Generic(path=ds / "links.csv", names_row=0),
        "movies": csv.Generic(path=ds / "movies.csv", names_row=0),
        "tags": csv.Generic(path=ds / "tags.csv", names_row=0),
    }
