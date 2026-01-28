Datamaestro Text Datasets
=========================

This section lists the datasets available through the datamaestro-text plugin.

Datasets are organized by domain:

- :doc:`ir` - Information retrieval benchmark collections (MS MARCO, TREC, etc.)
- :doc:`irds` - Integration with the `ir-datasets <https://ir-datasets.com/>`_ library
- :doc:`conversation` - Conversational search and query reformulation
- :doc:`text` - Raw text corpora
- :doc:`embeddings` - Pre-trained word embeddings
- :doc:`recommendation` - Rating and recommendation datasets

To load a dataset:

.. code-block:: python

   from datamaestro import prepare_dataset

   # Load by dataset ID
   dataset = prepare_dataset("com.microsoft.msmarco.passage")

To discover available datasets:

.. code-block:: bash

   # List all datasets
   datamaestro search text

   # Search by keyword
   datamaestro search "trec"

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   ir
   irds
   conversation
   text
   embeddings
   recommendation
