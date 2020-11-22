import logging
from datamaestro.data import File, data
from experimaestro import configmethod

@data()
class CoNLL_U(File):
    @configmethod
    def data(self):
        try:
            from conllu import parse
        except:
            logging.error("conllu python module not installed")
            raise

        with self.path.open("r", encoding="utf-8") as data_file:
            return parse(data_file.read())

    @configmethod
    def __iter__(self):
        try:
            from conllu import parse_incr
        except:
            logging.error("conllu python module not installed")
            raise

        with self.path.open("r", encoding="utf-8") as data_file:
            for tokenlist in parse_incr(data_file):
                yield tokenlist
