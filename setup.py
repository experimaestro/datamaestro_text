from pathlib import Path
import re
import sys
try:
    from setuptools import setup, find_namespace_packages
except ImportError:
    print("Please upgrade pip: find_namesspace_packages not found")
    sys.exit(1)

RE_BLANCK=re.compile(r"^\s*(#.*)?$")
with (Path(__file__).parent / 'requirements.txt').open() as f:
    requirements = [x for x in f.read().splitlines() if not RE_BLANCK.match(x)]


setup(
    name='datamaestro_text',
    version='0.4',
    description='Text related datasets',
    author='Benjamin Piwowarski',
    author_email='benjamin@piwowarski.fr',
    url='https://github.com/bpiwowar/datamaestro_texts',
    license='MIT',
    python_requires='>=3.5',
    packages=find_namespace_packages(include="datamaestro_text.*"),

    package_data={
        '': [ '*.yaml' ]
    },
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

    test_suite='datamaestro_text.test'
)
