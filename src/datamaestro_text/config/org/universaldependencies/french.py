from datamaestro.definitions import Dataset, dataset
from datamaestro.data.ml import Supervised
from datamaestro_text.data.tagging import CoNLL_U
from datamaestro.download.archive import ZipDownloader


# --- gsd


# description: |

# tasks: [ "POS parsing", "dependency parsing" ]
# tags: [ "french" ]

# files:
#   readme: README.md
#   stats: stats.xml
#   train: !@tagging:CoNLL_U
#     path: fr_gsd-ud-train.conllu
#   dev: !@tagging:CoNLL_U
#     path: fr_gsd-ud-dev.conllu
#   test: !@tagging:CoNLL_U
#     path: fr_gsd-ud-test.conllu


@dataset(url="https://github.com/UniversalDependencies/UD_French-GSD")
class Gsd(Dataset):
    """French GSD

    The UD_French-GSD was converted in 2015 from the content head version of the
    universal dependency treebank v2.0 (https://github.com/ryanmcd/uni-dep-tb). It
    is updated since 2015 independently from the previous source.
    """

    DS = ZipDownloader(
        "ds",
        "https://codeload.github.com/UniversalDependencies/UD_French-GSD/zip/master",
    )

    def config(self) -> Supervised:
        return Supervised.C(
            train=CoNLL_U.C(path=self.DS.path / "fr_gsd-ud-train.conllu"),
            test=CoNLL_U.C(path=self.DS.path / "fr_gsd-ud-dev.conllu"),
            validation=CoNLL_U.C(path=self.DS.path / "fr_gsd-ud-test.conllu"),
        )


# --- partut

# # See documentation on https://datamaestro.readthedocs.io

# # Configuration
# # See https://datamaestro.readthedocs.ioconfiguration/

# name: UD_French-ParTUT
# web: https://github.com/UniversalDependencies/UD_French-ParTUT

# description: |
#   UD_French-ParTUT is a conversion of a multilingual parallel treebank developed
#   at the University of Turin, and consisting of a variety of text genres,
#   including talks, legal texts and Wikipedia articles, among others.

# tasks: [ "POS parsing", "dependency parsing" ]
# tags: [ "french" ]


# # Describe how to download
# # See https://datamaestro.readthedocs.iodownload/

# download: !@/archive:Zip
#   url: https://codeload.github.com/UniversalDependencies/UD_French-ParTUT/zip/master

# files:
#   readme: README.md
#   stats: stats.xml
#   train: !@tagging:CoNLL_U
#     path: fr_partut-ud-train.conllu
#   dev: !@tagging:CoNLL_U
#     path: fr_partut-ud-dev.conllu
#   test: !@tagging:CoNLL_U
#     path: fr_partut-ud-test.conllu
