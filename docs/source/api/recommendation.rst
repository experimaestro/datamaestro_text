Recommendation
==============

This module provides data types for recommendation and rating datasets.

These datasets are commonly used for collaborative filtering and
recommendation system research.


Base Types
----------

.. autoxpmconfig:: datamaestro_text.data.recommendation.RatedItems

Base class for datasets containing user ratings. The ``ratings`` attribute
provides access to the ratings file.


MovieLens
---------

.. autoxpmconfig:: datamaestro_text.data.recommendation.Movielens

MovieLens datasets include additional metadata:

- ``ratings`` - User ratings (user_id, movie_id, rating, timestamp)
- ``movies`` - Movie metadata (movie_id, title, genres)
- ``tags`` - User-applied tags (user_id, movie_id, tag, timestamp)
- ``links`` - Links to external sources (movie_id, imdb_id, tmdb_id)

Example usage:

.. code-block:: python

   from datamaestro import prepare_dataset

   # Load MovieLens dataset
   ml = prepare_dataset("io.grouplens.movielens.ml1m")

   # Access ratings file
   ratings_path = ml.ratings.path

   # Access movie metadata
   movies_path = ml.movies.path
