from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(

    name='coinswitch-client',  # Required
    version='0.0.1',  # Required
    description='A simple coinswitch (v1,v2) client api',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/Willena/PythonCoinSwitchClient',  # Optional
    author='Guillaume VILLENA',  # Optional
    author_email='contact@guillaumevillena.fr',  # Optional

    # https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='api lib library coinswicth client cryptos',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    install_requires=['requests'],  # Optional
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/Willena/PythonCoinSwitchClient/issues',
        'Funding': 'https://paypal.me/GuillaumeVillena',
        'Say Thanks!': 'https://paypal.me/GuillaumeVillena',
        'Source': 'https://github.com/Willena/PythonCoinSwitchClient',
    },
)
