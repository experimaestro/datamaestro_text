# See documentation on https://datamaestro.readthedocs.io

from pathlib import Path
from datamaestro.definitions import datatags, dataset
from datamaestro_text.data.debate import GrandDebatFile
from datamaestro.download.single import filedownloader
from datamaestro.utils import HashCheck
from datamaestro.stream import Transform
import io
import json
import ijson
import os
import threading


class JsonToJsonl(Transform):
    """Transforms a JSON file with an array into a JSONL file with one line per
    array element"""

    def __call__(self, fileobj: io.IOBase) -> io.IOBase:
        # Stream items from the top-level array into a read-end pipe.
        try:
            fileobj.seek(0)
        except Exception:
            pass

        r_fd, w_fd = os.pipe()
        r_file = os.fdopen(r_fd, "rb")
        w_file = os.fdopen(w_fd, "wb")

        def _writer(fin, fout):
            try:
                for item in ijson.items(fin, "item"):
                    line = json.dumps(item, ensure_ascii=False) + "\n"
                    fout.write(line.encode("utf-8"))
                fout.close()
            except Exception:
                try:
                    fout.close()
                except Exception:
                    pass

        t = threading.Thread(target=_writer, args=(fileobj, w_file), daemon=True)
        t.start()

        return r_file


@filedownloader(
    "la_transition_ecologique_2019_03_21.jsonl",
    "http://opendata.auth-6f31f706db6f4a24b55f42a6a79c5086.storage.sbg.cloud.ovh.net/2019-03-21/LA_TRANSITION_ECOLOGIQUE.json",
    checker=HashCheck("c4ed3a8b8c43d5806d1f090e03f7aa91"),
    transforms=JsonToJsonl(),
)
@datatags("politics", "debate", "french")
@dataset(
    GrandDebatFile,
    url="https://granddebat.fr",
)
def transition(la_transition_ecologique_2019_03_21: Path):
    """Grand Débat National (transition écologique)

    The *Grand Débat National* (GDN) is a country-wide citizen consultation held
    in France in 2019.


    The consultation prompted citizens to express their views across four main
    themes: *Taxation and public spending*, *Organization of the state and
    public services*, *Democracy and citizenship*, and *Ecological transition*.
    A significant portion of this consultation involved online questionnaires,
    each concluding with a critical open-ended prompt: "Do you have anything to
    add about [theme]?".
    """
    return GrandDebatFile.C(path=la_transition_ecologique_2019_03_21)


@filedownloader(
    "fiscalité_et_dépenses_publiques_2019_03_21.jsonl",
    "http://opendata.auth-6f31f706db6f4a24b55f42a6a79c5086.storage.sbg.cloud.ovh.net/2019-03-21/LA_FISCALITE_ET_LES_DEPENSES_PUBLIQUES.json",
    checker=HashCheck("c4ed3a8b8c43d5806d1f090e03f7aa91"),
    transforms=JsonToJsonl(),
)
@datatags("politics", "debate", "french")
@dataset(
    GrandDebatFile,
    url="https://granddebat.fr",
)
def fiscalité(fiscalité_et_dépenses_publiques_2019_03_21: Path):
    """Grand Débat National (fiscalité et dépenses publiques)

    The *Grand Débat National* (GDN) is a country-wide citizen consultation held
    in France in 2019.


    The consultation prompted citizens to express their views across four main
    themes: *Taxation and public spending*, *Organization of the state and
    public services*, *Democracy and citizenship*, and *Ecological transition*.
    A significant portion of this consultation involved online questionnaires,
    each concluding with a critical open-ended prompt: "Do you have anything to
    add about [theme]?".
    """
    return GrandDebatFile.C(path=fiscalité_et_dépenses_publiques_2019_03_21)


@filedownloader(
    "democratie_et_citoyennete_2019_03_21.jsonl",
    "http://opendata.auth-6f31f706db6f4a24b55f42a6a79c5086.storage.sbg.cloud.ovh.net/2019-03-21/DEMOCRATIE_ET_CITOYENNETE.json",
    checker=HashCheck("049aaeca7e51747f2da5d68143c760fa"),
    transforms=JsonToJsonl(),
)
@datatags("politics", "debate", "french")
@dataset(
    GrandDebatFile,
    url="https://granddebat.fr",
)
def démocratie(democratie_et_citoyennete_2019_03_21: Path):
    """Grand Débat National (démocratie et citoyenneté)

    The *Grand Débat National* (GDN) is a country-wide citizen consultation held
    in France in 2019.


    The consultation prompted citizens to express their views across four main
    themes: *Taxation and public spending*, *Organization of the state and
    public services*, *Democracy and citizenship*, and *Ecological transition*.
    A significant portion of this consultation involved online questionnaires,
    each concluding with a critical open-ended prompt: "Do you have anything to
    add about [theme]?".
    """
    return GrandDebatFile.C(path=democratie_et_citoyennete_2019_03_21)


@filedownloader(
    "organisation_etat_services_publics_2019_03_21.jsonl",
    "http://opendata.auth-6f31f706db6f4a24b55f42a6a79c5086.storage.sbg.cloud.ovh.net/2019-03-21/ORGANISATION_DE_LETAT_ET_DES_SERVICES_PUBLICS.json",
    checker=HashCheck("0ccb7c401889f738b73b0caab897a68b"),
    transforms=JsonToJsonl(),
)
@datatags("politics", "debate", "french")
@dataset(
    GrandDebatFile,
    url="https://granddebat.fr",
)
def organisation(organisation_etat_services_publics_2019_03_21: Path):
    """Grand Débat National (organisation de l'État et des services publics)

    The *Grand Débat National* (GDN) is a country-wide citizen consultation held
    in France in 2019.


    The consultation prompted citizens to express their views across four main
    themes: *Taxation and public spending*, *Organization of the state and
    public services*, *Democracy and citizenship*, and *Ecological transition*.
    A significant portion of this consultation involved online questionnaires,
    each concluding with a critical open-ended prompt: "Do you have anything to
    add about [theme]?".
    """
    return GrandDebatFile.C(path=organisation_etat_services_publics_2019_03_21)


@filedownloader(
    "les_evenements_2019_03_21.jsonl",
    "http://opendata.auth-6f31f706db6f4a24b55f42a6a79c5086.storage.sbg.cloud.ovh.net/2019-03-21/LES_EVENEMENTS.json",
    checker=HashCheck("c4ed3a8b8c43d5806d1f090e03f7aa91"),
    transforms=JsonToJsonl(),
)
@datatags("politics", "debate", "french")
@dataset(
    GrandDebatFile,
    url="https://granddebat.fr",
)
def evenements(les_evenements_2019_03_21: Path):
    """Grand Débat National (événements)

    The *Grand Débat National* (GDN) is a country-wide citizen consultation held
    in France in 2019.


    The consultation prompted citizens to express their views across four main
    themes: *Taxation and public spending*, *Organization of the state and
    public services*, *Democracy and citizenship*, and *Ecological transition*.
    A significant portion of this consultation involved online questionnaires,
    each concluding with a critical open-ended prompt: "Do you have anything to
    add about [theme]?".
    """
    return GrandDebatFile.C(path=les_evenements_2019_03_21)
