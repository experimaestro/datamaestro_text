Information Retrieval API
=========================

This module provides data types for Information Retrieval datasets and experiments.

The core abstractions are:

- **Documents** - Collections of documents to be searched
- **Topics** - Queries or information needs
- **Assessments** - Relevance judgments (qrels) linking topics to relevant documents
- **Adhoc** - A complete IR test collection combining documents, topics, and assessments

For training neural rankers:

- **TrainingTriplets** - Training data as (query, positive_doc, negative_doc) triplets
- **PairwiseSampleDataset** - General pairwise training data


Data objects
------------

.. automodule:: datamaestro_text.data.ir.base
   :members:

Collection
----------

.. autoxpmconfig:: datamaestro_text.data.ir.Adhoc
.. autoxpmconfig:: datamaestro_text.datasets.irds.data.Adhoc

Topics
------

.. autoxpmconfig:: datamaestro_text.data.ir.Topics
    :members: iter, count

.. autoxpmconfig:: datamaestro_text.data.ir.csv.Topics
.. autoxpmconfig:: datamaestro_text.data.ir.TopicsStore

.. autoxpmconfig:: datamaestro_text.transforms.ir.TopicWrapper

Dataset-specific Topics
-----------------------

.. autoxpmconfig:: datamaestro_text.data.ir.trec.TrecTopics
.. autoxpmconfig:: datamaestro_text.data.ir.cord19.Topics
.. autoxpmconfig:: datamaestro_text.datasets.irds.data.Topics

Documents
---------

.. autoxpmconfig:: datamaestro_text.data.ir.Documents
    :members: iter_documents, iter_ids, documentcount
.. autoxpmconfig:: datamaestro_text.data.ir.csv.Documents
.. autoxpmconfig:: datamaestro_text.datasets.irds.data.LZ4DocumentStore
.. autoxpmconfig:: datamaestro_text.datasets.irds.data.LZ4JSONLDocumentStore


IR-Datasets Base
----------------

.. autoxpmconfig:: datamaestro_text.datasets.irds.data.IRDSId


Dataset-specific documents
**************************

.. autoxpmconfig:: datamaestro_text.data.ir.cord19.Documents
.. autoxpmconfig:: datamaestro_text.data.ir.trec.TipsterCollection
.. autoxpmconfig:: datamaestro_text.data.ir.stores.OrConvQADocumentStore
.. autoxpmconfig:: datamaestro_text.data.ir.stores.IKatClueWeb22DocumentStore
.. autoxpmconfig:: datamaestro_text.datasets.irds.data.Documents

Assessments
-----------

.. autoxpmconfig:: datamaestro_text.data.ir.AdhocAssessments
    :members:

.. autoxpmconfig:: datamaestro_text.data.ir.trec.TrecAdhocAssessments
.. autoxpmconfig:: datamaestro_text.datasets.irds.data.AdhocAssessments

.. autoclass:: datamaestro_text.data.ir.AdhocAssessedTopic
.. autoclass:: datamaestro_text.data.ir.AdhocAssessment

Runs
----

.. autoxpmconfig:: datamaestro_text.data.ir.AdhocRun
.. autoxpmconfig:: datamaestro_text.data.ir.csv.AdhocRunWithText
.. autoxpmconfig:: datamaestro_text.data.ir.trec.TrecAdhocRun
.. autoxpmconfig:: datamaestro_text.datasets.irds.data.AdhocRun


Results
-------

.. autoxpmconfig:: datamaestro_text.data.ir.AdhocResults
.. autoxpmconfig:: datamaestro_text.data.ir.trec.TrecAdhocResults
    :members: get_results

Evaluation
----------

.. autoxpmconfig:: datamaestro_text.data.ir.Measure


Reranking
---------

.. autoxpmconfig:: datamaestro_text.data.ir.RerankAdhoc

Document Index
---------------

.. autoxpmconfig:: datamaestro_text.data.ir.DocumentStore
    :members: documentcount, docid_internal2external, document_int, document_ext, iter_sample

.. autoxpmconfig:: datamaestro_text.data.ir.AdhocIndex
    :members: termcount, term_df


Training triplets
-----------------


.. autoxpmconfig:: datamaestro_text.data.ir.TrainingTriplets
    :members: iter

.. autoxpmconfig:: datamaestro_text.data.ir.PairwiseSampleDataset
    :members: iter

.. autoxpmconfig:: datamaestro_text.data.ir.TrainingTripletsLines

.. autoxpmconfig:: datamaestro_text.data.ir.huggingface.HuggingFacePairwiseSampleDataset
.. autoxpmconfig:: datamaestro_text.datasets.irds.data.TrainingTriplets

Transforms
**********

.. autoxpmconfig:: datamaestro_text.transforms.ir.StoreTrainingTripletTopicAdapter

.. autoxpmconfig:: datamaestro_text.transforms.ir.StoreTrainingTripletDocumentAdapter

.. autoxpmconfig:: datamaestro_text.transforms.ir.ShuffledTrainingTripletsLines
