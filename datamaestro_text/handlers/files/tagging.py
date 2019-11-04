import logging
from datamaestro.handlers.files import File

class CoNLL_U(File):
    def data(self):
        try:
            from conllu import parse_incr
        except:
            logging.error("conllu python module not installed")
            raise 

        data_file = self.path.open("r", encoding="utf-8")
        for tokenlist in parse_incr(data_file):
            yield tokenlist
