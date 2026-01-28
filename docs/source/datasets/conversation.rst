Conversational IR Datasets
==========================

This section lists datasets for conversational information retrieval
and contextual query understanding tasks.


Contextual Query Rewriting
--------------------------

These datasets contain conversational queries that need to be rewritten
to be self-contained (decontextualization), resolving coreferences and
ellipses from the conversation context.


CANARD
~~~~~~

Context-dependent Query Rewriting dataset for conversational question answering.
Contains queries from QuAC that have been manually rewritten to be self-contained.

.. dm:datasets:: com.github.aagohary.canard text

Example:

.. code-block:: python

   from datamaestro import prepare_dataset

   canard = prepare_dataset("com.github.aagohary.canard.train")
   for entry in canard.iter():
       print(f"Original: {entry.source}")
       print(f"Rewritten: {entry.rewrite}")


OrConvQA
~~~~~~~~

Open-Retrieval Conversational Question Answering dataset.
Contains multi-turn QA conversations with passage retrieval.

.. dm:datasets:: com.github.prdwb.orconvqa text


QReCC
~~~~~

Question Rewriting in Conversational Context dataset.
Contains conversations with human rewrites of questions.

.. dm:datasets:: com.github.apple.ml-qrecc text
