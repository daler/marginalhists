import ez_setup
ez_setup.use_setuptools()

import os
import sys
from setuptools import setup

version_py = os.path.join(os.path.dirname(__file__), 'marginalhists', 'version.py')
version = open(version_py).read().strip().split('=')[-1].replace('"','')

long_description = """
Flexible plotting of multiple series of scatters along with stacked marginal
histograms.
"""

setup(
        name="marginalhists",
        version=version,
        install_requires=['matplotlib'],
        packages=['marginalhists'],
        author="",
        description='scatter plots with marginal histograms',
        long_description=long_description,
        url="none",
        package_dir = {"marginalhists": "marginalhists"},
        author_email="dalerr@niddk.nih.gov",
        classifiers=['Development Status :: 4 - Beta'],
    )
