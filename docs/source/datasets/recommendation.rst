Recommendation Datasets
=======================

Datasets for recommendation systems and sentiment analysis.


IMDB Reviews
------------

The `ACL IMDB <https://ai.stanford.edu/~amaas/data/sentiment/>`_ dataset for
sentiment classification. Contains movie reviews labeled as positive or negative.

.. dm:datasets:: edu.stanford.aclimdb text

Example usage:

.. code-block:: python

   from datamaestro import prepare_dataset

   # Load IMDB sentiment dataset
   imdb = prepare_dataset("edu.stanford.aclimdb")

   # Access training and test data
   train = imdb.train
   test = imdb.test
