from pathlib import Path
from datamaestro.data import File, data, argument
from datamaestro.definitions import datatags
import numpy as np


@datatags("word embeddings")
@argument("encoding", str, ignored=True, default="utf-8")
@data(description="Word embeddings as a text word / values")
class WordEmbeddingsText(File):
    def load(self):
        words = {}
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
                words[word] = ix
        return words, np.matrix(vectors)
