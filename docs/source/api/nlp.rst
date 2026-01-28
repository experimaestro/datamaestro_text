NLP
===

This module provides data types for Natural Language Processing datasets,
particularly those involving linguistic annotations.


CoNLL-U Format
--------------

The `CoNLL-U format <https://universaldependencies.org/format.html>`_ is a
standard format for annotated linguistic data used in Universal Dependencies
and other NLP tasks.

.. autoxpmconfig:: datamaestro_text.data.tagging.CoNLL_U

CoNLL-U files contain token-level annotations including:

- Word forms and lemmas
- Universal POS tags and language-specific POS tags
- Morphological features
- Dependency relations (head and deprel)
- Miscellaneous annotations

Example CoNLL-U format::

   # sent_id = 1
   # text = The dog runs.
   1    The    the    DET    DT    _    2    det    _    _
   2    dog    dog    NOUN   NN    _    3    nsubj  _    _
   3    runs   run    VERB   VBZ   _    0    root   _    _
   4    .      .      PUNCT  .     _    3    punct  _    _
