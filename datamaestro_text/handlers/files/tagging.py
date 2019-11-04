import logging
from datamaestro.handlers.files import File

class CoNLL_U(File):
    def data(self, generator=False):
        try:
            from conllu import parse_incr, parse
        except:
            logging.error("conllu python module not installed")
            raise 

        data_file = self.path.open("r", encoding="utf-8")

        if not generator:
            return parse(data_file)
            
        for tokenlist in parse_incr(data_file):
            yield tokenlist
