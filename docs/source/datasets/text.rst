Text Datasets
=============

This section lists datasets consisting of raw text corpora,
useful for language model pre-training and other NLP tasks.


BookCorpus
----------

The BookCorpus dataset contains text from thousands of free books from
`Smashwords <https://www.smashwords.com/>`_. It was originally used for
training models like GPT and BERT.

.. dm:datasets:: com.smashwords.bookcorpus

Example usage:

.. code-block:: python

   from datamaestro import prepare_dataset

   dataset = prepare_dataset("com.smashwords.bookcorpus")
   # Access the text folder
   text_folder = dataset.path
