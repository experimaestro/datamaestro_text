from pathlib import Path
import http.client
import time
import logging
import zipfile
from tqdm import tqdm
import hashlib
import shutil
from collections import namedtuple

from datamaestro.download import Download
from datamaestro import DatasetDefinition
from datamaestro.utils import TemporaryDirectory

APIKEY_KEY = "org.themoviedb.apikey"


class Handler(Download):
    """Download using the TMDB API"""

    def __init__(self, dataset: DatasetDefinition, definition):
        super().__init__(dataset, definition)
        self.apikey = self.repository.context.preference(APIKEY_KEY)
        self.reset = 0
        self.remaining = 1

    def path(self, destination: Path):
        return destination.with_suffix(".zip")

    def retrieve(self, movieId):
        """Retrieves movie information in JSON (as a string) format"""

        while True:
            conn = http.client.HTTPSConnection("api.themoviedb.org")
            if self.reset >= time.time() and self.remaining == 0:
                logging.info("Waiting %.0f seconds", self.reset - time.time())
                time.sleep(self.reset - time.time())
            else:
                conn.request(
                    "GET",
                    "/3/movie/%s?language=en-US&api_key=%s" % (movieId, self.apikey),
                    "{}",
                )
                res = conn.getresponse()
                self.reset = float(res.headers["x-ratelimit-reset"])
                self.remaining = int(res.headers["x-ratelimit-remaining"])
                if res.code == 200:
                    return res.read()
                if res.code == 401:
                    raise Exception(
                        "Unauthorized: add the api key in the preference file [{}]".format(
                            APIKEY_KEY
                        )
                    )
                if res.code == 403:
                    self.reset = float(res.headers["Retry-After"])
                    self.remaining = 0
                    logging.warn(
                        "Code a 403 code from the movie DB: retrying after %s",
                        self.reset,
                    )
                elif res.code == 404:
                    return None

                raise Exception("Error code not handled: %d" % (res.code))


class MovieLens(Handler):
    def download(self, destination: Path):
        parent = self.dataset.parent

        cachepath = self.context.cachepath / (
            hashlib.sha256(self.dataset.id.encode("utf-8")).hexdigest() + ".zip"
        )
        logging.info("Retrieve items from moviedb.org (cache: %s)", cachepath)

        with zipfile.ZipFile(
            cachepath, mode="a", compression=zipfile.ZIP_DEFLATED
        ) as z:
            # Retrieve already downloaded items from Zip file
            done = set()
            for info in z.infolist():
                done.add(info.filename)
            if done:
                logging.info("Retrieved %d items from cache", len(done))

            # Gather items to download
            Item = namedtuple("Item", ["tmdbId", "movieId"])
            logging.debug("Reading the movie IDs to download")
            items = []
            with (parent.datadir / "links.csv").open("r") as fp:
                header = {x: i for i, x in enumerate(fp.readline().strip().split(","))}
                tmbdIx = header["tmdbId"]
                movieIx = header["movieId"]

                for line in fp:
                    fields = line.strip().split(",")
                    movieId = fields[movieIx]
                    if movieId not in done:
                        items.append(Item(movieId=movieId, tmdbId=fields[tmbdIx]))

            # Download from Movie DB
            logging.info("Downloading from movie DB")
            for item in tqdm(items):
                data = self.retrieve(item.tmdbId)
                if data is not None:
                    z.writestr(item.movieId, data)

        shutil.move(cachepath, self.path(destination))
