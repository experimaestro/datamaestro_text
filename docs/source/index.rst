Datamaestro Text
================

**datamaestro-text** is a `datamaestro <https://github.com/bpiwowar/datamaestro>`_ plugin that provides
access to text-related datasets for research in:

* **Information Retrieval (IR)** - Document collections, topics, relevance judgments, training triplets
* **Natural Language Processing (NLP)** - Text corpora, tagging datasets
* **Conversational IR** - Query rewriting, conversational search datasets
* **Word Embeddings** - Pre-trained word vectors (GloVe, etc.)
* **Recommendation** - Rating datasets (MovieLens, IMDB)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   api/index
   datasets/index


Installation
------------

Install from PyPI:

.. code-block:: bash

   pip install datamaestro-text

For development:

.. code-block:: bash

   git clone https://github.com/bpiwowar/datamaestro-text.git
   cd datamaestro-text
   pip install -e ".[dev]"


Quick Start
-----------

List available datasets:

.. code-block:: bash

   # List all datasets in the text repository
   datamaestro search text

   # Search for specific datasets
   datamaestro search "msmarco"

Load a dataset in Python:

.. code-block:: python

   from datamaestro import prepare_dataset

   # Load MS MARCO passage dataset
   dataset = prepare_dataset("com.microsoft.msmarco.passage")

   # Access documents, topics, and relevance judgments
   for doc in dataset.documents.iter_documents():
       print(doc[IDItem].id, doc[TextItem].text)

The plugin also provides access to the `ir-datasets <https://ir-datasets.com/>`_ library
through the ``irds`` namespace:

.. code-block:: python

   # Load via ir-datasets integration
   dataset = prepare_dataset("irds.msmarco-passage")


Key Concepts
------------

**Data Types**
   Schema classes that define the structure of datasets (e.g., ``Documents``, ``Topics``, ``Adhoc``).
   See the :doc:`api/index` for the complete API reference.

**Dataset Configurations**
   Specific dataset definitions that implement data types with download URLs and processing logic.
   See :doc:`datasets/index` for available datasets.

**Records and Items**
   Typed data containers using the experimaestro record system. Common items include
   ``IDItem`` (identifiers) and ``TextItem`` (text content).


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
