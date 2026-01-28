IR-Datasets Integration
=======================

Datamaestro-text provides an interface to the `ir-datasets <https://ir-datasets.com/>`_
library, giving access to hundreds of IR benchmarks through a unified API.

Install ir-datasets:

.. code-block:: bash

   pip install ir-datasets

Usage:

.. code-block:: python

   from datamaestro import prepare_dataset

   # Load any ir-datasets collection via the irds namespace
   dataset = prepare_dataset("irds.msmarco-passage")

   # Same API as native datasets
   for doc in dataset.documents.iter_documents():
       print(doc)

The list below is auto-generated and may not reflect the exact version
of ir-datasets installed on your system.


Data Types
----------

These wrapper types provide the datamaestro interface for ir-datasets data:

.. autoxpmconfig:: datamaestro_text.datasets.irds.data.Topics
.. autoxpmconfig:: datamaestro_text.datasets.irds.data.Documents
.. autoxpmconfig:: datamaestro_text.datasets.irds.data.AdhocAssessments

See also :class:`~datamaestro_text.datasets.irds.data.LZ4DocumentStore` in the :doc:`/api/ir` section.


Available Datasets
------------------

.. dm:repository:: irds
