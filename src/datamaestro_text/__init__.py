import datamaestro

from .version import version, version_tuple


class Repository(datamaestro.Repository):
    AUTHOR = """Benjamin Piwowarski <benjamin@piwowarski.fr>"""
    DESCRIPTION = """Text datasets repository"""
    NAMESPACE = """text"""
