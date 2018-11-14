from setuptools import setup, find_packages

setup(
    name='datamaestro_text',
    version='0.1',
    description='Text related datasets',
    author='Benjamin Piwowarski',
    author_email='benjamin@piwowarski.fr',
    url='https://github.com/bpiwowar/datamaestro_texts',
    license='MIT',
    python_requires='>=3.5',
    packages=["datamaestro_text"],
    install_requires=[
        'datamaestro'
    ],
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

    }
)
