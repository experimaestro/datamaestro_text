Word Embeddings
===============

Pre-trained word embeddings for NLP tasks.


GloVe
-----

`GloVe <https://nlp.stanford.edu/projects/glove/>`_ (Global Vectors for Word Representation)
embeddings from Stanford NLP. Available in multiple dimensions (50, 100, 200, 300)
trained on different corpora.

.. dm:datasets:: edu.stanford.glove text

Example usage:

.. code-block:: python

   from datamaestro import prepare_dataset

   # Load 100-dimensional GloVe trained on Wikipedia + Gigaword
   glove = prepare_dataset("edu.stanford.glove.6b.100")

   # Load embeddings into memory
   words, vectors = glove.load()

   # Create lookup dictionary
   word_to_idx = {w: i for i, w in enumerate(words)}

   # Get embedding for a word
   idx = word_to_idx.get("example")
   if idx is not None:
       embedding = vectors[idx]
