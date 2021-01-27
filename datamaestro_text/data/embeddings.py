from pathlib import Path
from datamaestro.data import File, data, argument
from datamaestro.definitions import datatags
import numpy as np
from typing import Tuple, List


@datatags("word embeddings")
@data(description="Generic class for word embeddings")
class WordEmbeddings:
    """Generic word embeddings"""

    def load(self) -> Tuple[List[str], np.matrix]:
        """Load the word embeddings

        Returns:
            The word dictionary and the matrix
        """
        raise NotImplementedError()


@argument("encoding", str, ignored=True, default="utf-8")
@data(description="Word embeddings as a text word / values")
class WordEmbeddingsText(WordEmbeddings, File):
    """Word embeddings"""

    def load(self):
        words = []
        vectors = []
        dimension = None
        with self.path.open("rt", encoding=self.encoding) as fp:
            for ix, line in enumerate(fp):
                word, *values = line.split(" ")
                vectors.append([float(x) for x in values])
                if dimension is None:
                    dimension = len(values)
                else:
                    assert dimension == len(values)
                words.append(word)
        return words, np.matrix(vectors)
