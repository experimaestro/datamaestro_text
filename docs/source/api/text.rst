Text API
========

This module provides data types for raw text datasets.

These types are used for datasets that provide text content without additional
structure (as opposed to IR datasets which have documents, topics, etc.).

Text Storage
------------

Basic containers for text data:

.. autoxpmconfig:: datamaestro_text.data.text.TextFolder

A folder containing text files. Access the path via the ``path`` attribute.

.. autoxpmconfig:: datamaestro_text.data.text.TextFile

A single file containing text content. Access the path via the ``path`` attribute.


Training Datasets
-----------------

For machine learning tasks with train/test splits:

.. autoxpmconfig:: datamaestro_text.data.text.TrainingText

A supervised learning dataset with train, test, and optional validation splits.

Example usage:

.. code-block:: python

   from datamaestro import prepare_dataset

   # Load a text training dataset
   dataset = prepare_dataset("org.allenai.bookcorpus")

   # Access the training data
   train_data = dataset.train
   test_data = dataset.test  # may be None
   validation_data = dataset.validation  # may be None
