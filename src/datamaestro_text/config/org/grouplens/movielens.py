from datamaestro.definitions import Dataset, dataset
from datamaestro.download.archive import ZipDownloader
import datamaestro.data.csv as csv
from datamaestro_text.data.recommendation import Movielens


@dataset(url="https://grouplens.org/datasets/movielens/latest/", timestamp=True)
class Small(Dataset):
    """MovieLens (small dataset)

    100,000 ratings and 3,600 tag applications applied to 9,000 movies by 600 users (as of 9/2018)
    """

    DS = ZipDownloader(
        "ds", "http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
    )

    def config(self) -> Movielens:
        return Movielens.C(
            ratings=csv.Generic.C(path=self.DS.path / "ratings.csv", names_row=0),
            links=csv.Generic.C(path=self.DS.path / "links.csv", names_row=0),
            movies=csv.Generic.C(path=self.DS.path / "movies.csv", names_row=0),
            tags=csv.Generic.C(path=self.DS.path / "tags.csv", names_row=0),
        )


@dataset(url="https://grouplens.org/datasets/movielens/latest/", timestamp=True)
class Full(Dataset):
    """MovieLens (full dataset)

    27,000,000 ratings and 1,100,000 tag applications applied to 58,000 movies by 280,000 users (as of 9/2018)
    """

    DS = ZipDownloader(
        "ds", "http://files.grouplens.org/datasets/movielens/ml-latest.zip"
    )

    def config(self) -> Movielens:
        return Movielens.C(
            ratings=csv.Generic.C(path=self.DS.path / "ratings.csv", names_row=0),
            links=csv.Generic.C(path=self.DS.path / "links.csv", names_row=0),
            movies=csv.Generic.C(path=self.DS.path / "movies.csv", names_row=0),
            tags=csv.Generic.C(path=self.DS.path / "tags.csv", names_row=0),
        )
