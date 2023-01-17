from typing import Iterator
from experimaestro import Meta
from datamaestro.data.huggingface import HuggingFaceDataset
from . import PairwiseSample, PairwiseSampleDataset


class HuggingFacePairwiseSampleDataset(HuggingFaceDataset, PairwiseSampleDataset):
    """Triplet for training IR systems: query / query ID, positive document, negative document

    Attributes:

        ids: True if the triplet is made of IDs, False otherwise
    """

    ids: Meta[bool]

    query_id: Meta[str] = "qid"
    """The name of the field containing the query ID"""

    pos_id: Meta[str] = "pos"
    """The name of the field containing the positive samples"""

    neg_id: Meta[str] = "neg"
    """The name of the field containing the negative samples"""

    def iter(self) -> Iterator[PairwiseSample]:
        for element in self.data:
            yield PairwiseSample(
                element[self.query_id], element[self.pos_id], element[self.neg_id]
            )
