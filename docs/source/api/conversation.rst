Conversation API
================

This module provides data types for conversational information retrieval
and query understanding tasks.

.. currentmodule:: datamaestro_text.data.conversation.base


Core Data Classes
-----------------

Entry types for conversation turns:

.. autoclass:: AnswerEntry
   :members:

.. autoclass:: RetrievedEntry
   :members:

.. autoclass:: ClarifyingQuestionEntry
   :members:

.. autoclass:: DecontextualizedItem
   :members:

Conversation structures:

.. autoclass:: ConversationHistory
   :members:

.. autoclass:: ConversationHistoryItem
   :members:


Conversational IR
-----------------

.. autoxpmconfig:: datamaestro_text.data.conversation.base.ConversationUserTopics


Contextual Query Reformulation
------------------------------

Base class for conversation datasets:

.. autoxpmconfig:: datamaestro_text.data.conversation.base.ConversationDataset


CANARD Dataset
~~~~~~~~~~~~~~

.. autoxpmconfig:: datamaestro_text.data.conversation.canard.CanardDataset


OrConvQA Dataset
~~~~~~~~~~~~~~~~

.. autoxpmconfig:: datamaestro_text.data.conversation.orconvqa.OrConvQADataset


QReCC Dataset
~~~~~~~~~~~~~

.. autoxpmconfig:: datamaestro_text.data.conversation.qrecc.QReCCDataset


iKAT Dataset
~~~~~~~~~~~~

.. autoxpmconfig:: datamaestro_text.data.conversation.ikat.IkatConversations
