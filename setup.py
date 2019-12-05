import os
from pathlib import Path
import re
import sys
try:
    from setuptools import setup, find_namespace_packages
except ImportError:
    print("Please upgrade pip: find_namespace_packages not found")
    sys.exit(1)
from setuptools.command.install import install

# Date-based versioning
VERSION='2019.12.5'

RE_BLANCK=re.compile(r"^\s*(#.*)?$")
with (Path(__file__).parent / 'requirements.txt').open() as f:
    requirements = [x for x in f.read().splitlines() if not RE_BLANCK.match(x)]

class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='datamaestro_text',
    version=VERSION,
    description='Text related datasets',
    author='Benjamin Piwowarski',
    author_email='benjamin@piwowarski.fr',
    url='https://github.com/bpiwowar/datamaestro_texts',
    license='MIT',
    python_requires='>=3.5',
    packages=find_namespace_packages(include="datamaestro_text.*"),
    long_description=long_description,
    long_description_content_type="text/markdown",

    install_requires=requirements,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    entry_points={
        'datamaestro.repositories': [
            'text = datamaestro_text:Repository'
        ]
    },
    cmdclass={
        'verify': VerifyVersionCommand,
    },
    test_suite='datamaestro_text.test'
)
