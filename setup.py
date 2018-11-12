from setuptools import setup, find_packages

setup(
    name='datasets_text',
    version='0.0.1',
    description='Information Access datasets',
    author='Benjamin Piwowarski',
    author_email='benjamin@piwowarski.fr',
    license='MIT',
    python_requires='>=3.5',
    install_requires=[
        'datasets'
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
        'datasets.repositories': [
            'text = datasets_text:Repository'
        ]

    }
)