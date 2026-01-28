Word Embeddings
===============

This module provides data types for pre-trained word embeddings.

Word embeddings are dense vector representations of words, useful for
NLP tasks, semantic similarity, and as input features for neural models.


Base Class
----------

.. autoxpmconfig:: datamaestro_text.data.embeddings.WordEmbeddings

Abstract base class for word embeddings. Provides the ``load()`` method
that returns a tuple of ``(words, vectors)`` where:

- ``words`` is a list of vocabulary words
- ``vectors`` is a numpy matrix where ``vectors[i]`` is the embedding for ``words[i]``


File-Based Embeddings
---------------------

.. autoxpmconfig:: datamaestro_text.data.embeddings.WordEmbeddingsText

Word embeddings stored in a text file with format: ``word value1 value2 ... valueN``

Example usage:

.. code-block:: python

   from datamaestro import prepare_dataset

   # Load GloVe embeddings (50-dimensional)
   glove = prepare_dataset("edu.stanford.glove.6b.50")

   # Load into memory
   words, vectors = glove.load()

   # Create a word-to-index mapping
   word_to_idx = {word: idx for idx, word in enumerate(words)}

   # Get embedding for a word
   if "computer" in word_to_idx:
       embedding = vectors[word_to_idx["computer"]]
       print(f"Embedding shape: {embedding.shape}")

   # Available GloVe variants:
   # - edu.stanford.glove.6b.50   (50d, trained on 6B tokens)
   # - edu.stanford.glove.6b.100  (100d)
   # - edu.stanford.glove.6b.200  (200d)
   # - edu.stanford.glove.6b.300  (300d)
