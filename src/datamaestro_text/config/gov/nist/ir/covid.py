"""CORD-19 dataset"""

from datamaestro.annotations.agreement import useragreement
from datamaestro.definitions import Dataset, datatasks, dataset
from datamaestro.download import reference
from datamaestro.download.single import FileDownloader
from datamaestro.utils import HashCheck
from datamaestro_text.data.ir import Adhoc
import datamaestro_text.data.ir.cord19 as d_cord19
from datamaestro_text.data.ir.trec import TrecAdhocAssessments

cord19_lua = useragreement(
    """COVID DATASET LICENSE AGREEMENT

By accessing, downloading or otherwise using any Journals, Articles, Metadata, Abstracts,
Full-Texts or any other content types provided in the COVID-19 Open Research Dataset (CORD-19)
Database (the "Data"), You expressly acknowledge and agree to the following:

\u2022 AI2 grants to You a worldwide, perpetual, non-exclusive, non-transferablelicenseto use and
make derivatives of the Datafor text and data mining only.

\u2022 AI2 warrants that it has the right to make the Data available to Youas provided for in and
subject to this Agreement and in accordance with applicable law.  EXCEPT FOR THE LIMITED WARRANTY
IN THIS SECTION, THE DATA IS PROVIDED "AS IS", WITHOUT ANY WARRANTIES OF ANY KIND.

\u2022 You agree to comply with all applicable local, state, national, and international laws and
regulations with respect to AI2's license and Youruse of the Data.\u2022 Data provided by AI2 is
from copyrighted sources of the respective copyright holders. You are solely responsible
for Your and Your users' compliance with any copyright, patent or trademark restrictions
and are referred to the copyright, patent or trademark notices appearing in the original
sources, all of which are hereby incorporated by reference""",
    id="ai2.cord19",
)


@cord19_lua
@dataset(
    url="https://ir.nist.gov/covidSubmit/index.html",
)
class Cord19Round5Metadata(Dataset):
    """Cord 19 metadata (round 5)

    Released on 2020-07-16
    """

    DATA = FileDownloader(
        "data.csv",
        url="https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-07-16/metadata.csv",
        checker=HashCheck("80d664e496b8b7e50a39c6f6bb92e0ef"),
    )

    def config(self) -> d_cord19.Documents:
        return d_cord19.Documents.C(
            path=self.DATA.path,
            names_row=0,
            # Number of documents
            count=192509,
        )


@dataset()
class Cord19Round5Topics(Dataset):
    """CORD-19 topics (round 5)"""

    DATA = FileDownloader(
        "data.xml",
        url="https://ir.nist.gov/covidSubmit/data/topics-rnd5.xml",
        checker=HashCheck("0307a37b6b9f1a5f233340a769d538ea"),
    )

    def config(self) -> d_cord19.Topics:
        return d_cord19.Topics.C(path=self.DATA.path)


@dataset()
class Cord19Round5Assessments(Dataset):
    """CORD19 assessments (round 5)"""

    DATA = FileDownloader(
        "data.ssv",
        url="https://ir.nist.gov/covidSubmit/data/qrels-covid_d5_j0.5-5.txt",
        checker=HashCheck("8138424a59daea0aba751c8a891e5f54"),
    )

    def config(self) -> TrecAdhocAssessments:
        return TrecAdhocAssessments.C(path=self.DATA.path)


@datatasks("information retrieval", "passage retrieval")
@dataset(url="https://ir.nist.gov/covidSubmit/data.html")
class Cord19Round5(Dataset):
    """CORD-19 IR collection (round 5)

    This is the primary test collection for ad hoc retrieval that is the outcome of all five rounds of TREC-COVID. The test set, called TREC-COVID Complete, consists of the Round 5 document set (July 16 release of CORD-19); the final set of 50 topics; and the cumulative judgments from all assessing rounds with CORD-UIDs mapped to July 16 ids if necessary, previously judged documents no longer in the July 16 release removed, and the last judgments for documents judged multiple times due to significant content changes between rounds. Note that no TREC-COVID submissions correspond to this collection since all TREC-COVID submissions were subject to residual collection evaluation.
    """

    COLLECTION = reference(varname="collection", reference=Cord19Round5Metadata)
    TOPICS = reference(varname="topics", reference=Cord19Round5Topics)
    QRELS = reference(varname="qrels", reference=Cord19Round5Assessments)

    def config(self) -> Adhoc:
        return Adhoc.C(
            documents=self.COLLECTION.prepare(),
            topics=self.TOPICS.prepare(),
            assessments=self.QRELS.prepare(),
        )
