Grand Debat API
===============

This module provides data types for the French "Grand Debat National" dataset,
a large-scale public consultation conducted in France in 2019.

The dataset contains citizen contributions (opinions and responses) to
questions across four main themes: ecological transition, taxation, democracy
and citizenship, and state organization and public services.


Data Classes
------------

.. autoclass:: datamaestro_text.data.debate.granddebat.GrandDebatEntry
   :members:

Represents a single contribution with metadata (author info, timestamps)
and a list of responses to questions.

.. autoclass:: datamaestro_text.data.debate.granddebat.GrandDebatResponse
   :members:

Represents a response to a specific question in the consultation.


File Access
-----------

.. autoxpmconfig:: datamaestro_text.data.debate.granddebat.GrandDebatFile
   :members:

JSONL file containing Grand Debat contributions. Supports iteration over entries.

Example usage:

.. code-block:: python

   from datamaestro import prepare_dataset

   # Load Grand Debat dataset
   gd = prepare_dataset("fr.granddebat.democratie")

   # Iterate over contributions
   for entry in gd:
       print(f"Contribution {entry.id}: {entry.title}")
       print(f"  Author type: {entry.author_type}")
       print(f"  ZIP code: {entry.author_zip_code}")

       # Access responses to questions
       for response in entry.responses:
           print(f"  Q: {response.question_title}")
           print(f"  A: {response.formatted_value}")
