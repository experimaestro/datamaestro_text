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

Conversational IR
-----------------

.. autoxpmconfig:: datamaestro_text.data.conversation.base.ConversationUserTopics


Contextual query reformulation
------------------------------

.. autoxpmconfig:: datamaestro_text.data.conversation.base.ConversationDataset

.. autoclass:: ContextualizedRewrittenQuery
    :members:

CANARD Dataset

.. autoxpmconfig:: datamaestro_text.data.conversation.canard.CanardDataset
    :members: iter

OrConvQA Dataset

.. autoxpmconfig:: datamaestro_text.data.conversation.orconvqa.OrConvQADataset
    :members: iter

.. autoclass:: datamaestro_text.data.conversation.orconvqa.OrConvQADatasetAnswer
    :members:

.. autoclass:: datamaestro_text.data.conversation.orconvqa.OrConvQADatasetHistoryEntry
    :members:

QReCC Dataset

.. autoclass:: datamaestro_text.data.conversation.qrecc.QReCCDatasetEntry
    :members:

.. autoxpmconfig:: datamaestro_text.data.conversation.qrecc.QReCCDataset
    :members: iter


iKAT Dataset

.. autoclass:: datamaestro_text.data.conversation.ikat.IkatConversationTopic
    :members:

.. autoclass:: datamaestro_text.data.conversation.ikat.IkatConversationEntry
    :members:

.. autoxpmconfig:: datamaestro_text.data.conversation.ikat.IkatConversations
    :members: iter
