Information Retrieval Datasets
==============================

This section lists native IR dataset definitions. For access to hundreds
more IR datasets, see :doc:`irds` (ir-datasets integration).


MS MARCO Passage
----------------

The `MS MARCO <https://microsoft.github.io/msmarco/>`_ (Microsoft Machine Reading
Comprehension) Passage Ranking dataset. One of the most widely used benchmarks
for neural IR research.

Contains ~8.8M passages and ~500K training queries with sparse relevance judgments.

.. dm:datasets:: com.microsoft.msmarco.passage text

Example usage:

.. code-block:: python

   from datamaestro import prepare_dataset
   from datamaestro.record import IDItem, TextItem

   # Load the full adhoc dataset
   adhoc = prepare_dataset("com.microsoft.msmarco.passage")

   # Iterate over documents
   for doc in adhoc.documents.iter_documents():
       doc_id = doc[IDItem].id
       text = doc[TextItem].text

   # Load training triplets
   triplets = prepare_dataset("com.microsoft.msmarco.passage.train.idstriples.small")
   for triplet in triplets.iter():
       query = triplet.query
       pos_doc = triplet.positive
       neg_doc = triplet.negative


TREC Ad Hoc
-----------

Classic TREC Ad Hoc test collections from NIST. These collections have been
fundamental benchmarks in IR research since the 1990s.

.. dm:datasets:: gov.nist.trec.adhoc text

Example usage:

.. code-block:: python

   from datamaestro import prepare_dataset

   # Load TREC Adhoc dataset (e.g., TREC-8)
   adhoc = prepare_dataset("gov.nist.trec.adhoc.8")

   # Access components
   documents = adhoc.documents
   topics = adhoc.topics
   assessments = adhoc.assessments
