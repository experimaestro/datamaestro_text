Getting Started
===============

This guide shows how to use datamaestro-text to access datasets for your research.


Loading Datasets
----------------

All datasets are loaded using the ``prepare_dataset`` function:

.. code-block:: python

   from datamaestro import prepare_dataset

   # Load by dataset ID
   dataset = prepare_dataset("com.microsoft.msmarco.passage")

Dataset IDs follow a hierarchical naming convention based on their source
(e.g., ``com.microsoft.msmarco.passage`` for MS MARCO passage ranking).


Working with IR Datasets
------------------------

Information Retrieval datasets typically contain three components:

1. **Documents** - The collection of documents to search
2. **Topics** - Queries or information needs
3. **Assessments** - Relevance judgments (qrels)

Example with MS MARCO:

.. code-block:: python

   from datamaestro import prepare_dataset
   from datamaestro.record import IDItem, TextItem

   # Load the dataset
   adhoc = prepare_dataset("com.microsoft.msmarco.passage")

   # Iterate over documents
   for doc in adhoc.documents.iter_documents():
       doc_id = doc[IDItem].id
       doc_text = doc[TextItem].text
       print(f"Document {doc_id}: {doc_text[:100]}...")

   # Iterate over topics (queries)
   for topic in adhoc.topics.iter():
       topic_id = topic[IDItem].id
       query_text = topic[TextItem].text
       print(f"Query {topic_id}: {query_text}")

   # Access relevance judgments
   for assessed_topic in adhoc.assessments.iter():
       topic_id = assessed_topic.topic_id
       for assessment in assessed_topic.assessments:
           doc_id = assessment.doc_id
           relevance = assessment.rel


Using IR-Datasets Integration
-----------------------------

The plugin provides access to the `ir-datasets <https://ir-datasets.com/>`_ library
through the ``irds`` namespace. This gives access to hundreds of IR datasets:

.. code-block:: python

   from datamaestro import prepare_dataset

   # Load via ir-datasets
   dataset = prepare_dataset("irds.msmarco-passage")

   # Same interface as native datasets
   for doc in dataset.documents.iter_documents():
       print(doc[IDItem].id)

See :doc:`datasets/irds` for the full list of available ir-datasets.


Training Data for Neural IR
---------------------------

For training neural ranking models, use training triplets:

.. code-block:: python

   from datamaestro import prepare_dataset
   from datamaestro.record import TextItem

   # Load training triplets
   triplets = prepare_dataset("com.microsoft.msmarco.passage.train.idstriples.small")

   # Iterate over (query, positive, negative) triplets
   for triplet in triplets.iter():
       query = triplet.query[TextItem].text
       positive_doc = triplet.positive[TextItem].text
       negative_doc = triplet.negative[TextItem].text


Word Embeddings
---------------

Load pre-trained word embeddings:

.. code-block:: python

   from datamaestro import prepare_dataset

   # Load GloVe embeddings
   glove = prepare_dataset("edu.stanford.glove.6b.50")

   # Load word vectors
   words, vectors = glove.load()

   # vectors is a numpy matrix where vectors[i] is the embedding for words[i]
   print(f"Vocabulary size: {len(words)}")
   print(f"Embedding dimension: {vectors.shape[1]}")


Dataset Discovery
-----------------

Find available datasets from the command line:

.. code-block:: bash

   # List all text datasets
   datamaestro search text

   # Search by keyword
   datamaestro search "trec"
   datamaestro search "conversation"

   # Show dataset details
   datamaestro info com.microsoft.msmarco.passage

Or programmatically:

.. code-block:: python

   from datamaestro import Repository

   # Get the text repository
   repo = Repository.find("text")

   # List all dataset IDs
   for dataset_id in repo.datasetids():
       print(dataset_id)


User Agreements
---------------

Some datasets require accepting a user agreement before download.
When you first access such a dataset, datamaestro will prompt you to accept the terms.

You can pre-accept agreements:

.. code-block:: bash

   datamaestro prepare com.microsoft.msmarco.passage


Caching and Data Directory
--------------------------

Downloaded data is cached in ``~/.local/share/datamaestro`` by default.
You can change this by setting the ``DATAMAESTRO_DATA`` environment variable:

.. code-block:: bash

   export DATAMAESTRO_DATA=/path/to/data
