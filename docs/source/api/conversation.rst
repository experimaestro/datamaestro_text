Conversation API
================

.. currentmodule:: datamaestro_text.data.conversation

Data classes
------------

.. autoclass:: Entry
    :members:

.. autoclass:: DecontextualizedDictEntry
    :members:

.. autoclass:: AnswerEntry
    :members:

.. autoclass:: RetrievedEntry
    :members:

.. autoclass:: ClarifyingQuestionEntry
    :members:


.. autoclass:: Conversation

.. autoclass:: ConversationTopic

Contextual query reformulation
------------------------------

.. autoxpmconfig:: datamaestro_text.data.conversation.base.ConversationDataset

.. autoclass:: ContextualizedRewrittenQuery
    :members:

.. autoxpmconfig:: datamaestro_text.data.conversation.canard.CanardDataset
    :members: iter

.. autoxpmconfig:: datamaestro_text.data.conversation.orconvqa.OrConvQADataset
    :members: iter

.. autoclass:: datamaestro_text.data.conversation.orconvqa.OrConvQADatasetAnswer
    :members:

.. autoclass:: datamaestro_text.data.conversation.orconvqa.OrConvQADatasetHistoryEntry
    :members:



.. autoclass:: datamaestro_text.data.conversation.orconvqa.QReCCDatasetEntry
    :members:

.. autoxpmconfig:: datamaestro_text.data.conversation.qrecc.QReCCDataset
    :members: iter
