Information Retrieval API
=========================


Data objects
------------

.. automodule:: datamaestro_text.data.ir.base
   :members:

Collection
----------

.. autoxpmconfig:: datamaestro_text.data.ir.Adhoc

Topics
------

.. autoxpmconfig:: datamaestro_text.data.ir.Topics
    :members: iter, count

.. autoxpmconfig:: datamaestro_text.data.ir.csv.Topics

.. autoclass:: datamaestro_text.data.ir.Topic

Documents
---------
.. autoclass:: datamaestro_text.data.ir.Document

.. autoxpmconfig:: datamaestro_text.data.ir.Documents
    :members: iter_documents, iter_ids, documentcount
.. autoxpmconfig:: datamaestro_text.data.ir.cord19.Documents
.. autoxpmconfig:: datamaestro_text.data.ir.csv.Documents

Assessments
-----------

.. autoxpmconfig:: datamaestro_text.data.ir.AdhocAssessments
    :members:

.. autoxpmconfig:: datamaestro_text.data.ir.trec.TrecAdhocAssessments

.. autoclass:: datamaestro_text.data.ir.AdhocAssessedTopic
.. autoclass:: datamaestro_text.data.ir.AdhocAssessment

Runs
----

.. autoxpmconfig:: datamaestro_text.data.ir.AdhocRun
.. autoxpmconfig:: datamaestro_text.data.ir.csv.AdhocRunWithText
.. autoxpmconfig:: datamaestro_text.data.ir.trec.TrecAdhocRun

Results
-------

.. autoxpmconfig:: datamaestro_text.data.ir.trec.TrecAdhocResults
    :members: get_results


Reranking
---------

.. autoxpmconfig:: datamaestro_text.data.ir.RerankAdhoc

Document Index
---------------

.. autoxpmconfig:: datamaestro_text.data.ir.DocumentStore
    :members: documentcount, document_text, docid_internal2external, document, iter_sample

.. autoxpmconfig:: datamaestro_text.data.ir.AdhocIndex
    :members: termcount, term_df


Training triplets
-----------------


.. autoxpmconfig:: datamaestro_text.data.ir.TrainingTriplets
    :members: iter

.. autoxpmconfig:: datamaestro_text.data.ir.PairwiseSampleDataset
    :members: iter

.. autoxpmconfig:: datamaestro_text.data.ir.TrainingTripletsLines

.. autoxpmconfig:: datamaestro_text.data.ir.csv.TrainingTriplets
.. autoxpmconfig:: datamaestro_text.data.ir.csv.TrainingTripletsID

.. autoxpmconfig:: datamaestro_text.data.ir.huggingface.HuggingFacePairwiseSampleDataset
