import datamaestro

from .version import version as version, version_tuple as version_tuple


class Repository(datamaestro.Repository):
    AUTHOR = """Benjamin Piwowarski <benjamin@piwowarski.fr>"""
    DESCRIPTION = """Text datasets repository"""
    NAMESPACE = """text"""
