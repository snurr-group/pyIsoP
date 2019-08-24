"""
PyIsoP
A fast and accurate semi-analytic method for predicting small molecule adsorption in nanoporous
materials, ideal for high-throughput screening applications. Developed by Arun Gopalan at
R. Q. Snurr Research Group, Northwestern University.
"""
from setuptools import setup
import versioneer

DOCLINES = __doc__.split("\n")

setup(
    # Self-descriptive entries which should always be present
    name='pyIsoP',
    author='Arun Gopalan',
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES[2:]),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='BSD-3-Clause',

    # Which Python importable modules should be included when your package is installe  d
    packages=['pyIsoP', "pyIsoP.tests"],

    # Optional include package data to ship with your package
    # Comment out this line to prevent the files from being packaged with your software
    # Extend/modify the list to include/exclude other items as need be
    package_data={'pyIsoP': ["data/*.dat","data/*.joblib","data/*.cif","data/*.pdb","data/*.md"]},

    # Additional entries you may want simply uncomment the lines you want and fill in the data
    author_email='arungopalan2020@u.northwestern.edu',      # Author email
    # version='1.0.0',
    url='https://github.com/arung-northwestern/pyIsoP',  # Website
    install_requires=["numpy>=1.13.3", "ase==3.16", "tqdm>=4.15", "pyevtk==1.1.1","pandas>=0.20.3","numba>=0.35","scikit-learn>=0.19.1","scipy>=1.1.0","pytest>=5.0.1"],              # Required packages, pulls from pip if needed; do not use for Conda deployment
    platforms=['Linux','Unix', 'Windows'],            # Valid platforms your code works on, adjust to your flavor
    python_requires=">=3.6",          # Python version restrictions

    # Manual control if final package is compressible or not, set False to prevent the .egg from being made
    # zip_safe=False,
    
)
