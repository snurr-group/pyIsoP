.. pyisop documentation master file, created by
   sphinx-quickstart on Thu Mar 15 13:55:56 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. pyisop documentation master file, created by
   sphinx-quickstart on Thu Mar 15 13:55:56 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Python Isotherm Prediction (PyIsoP)
**************************************************
PyIsoP uses a fast and accurate, semi-analytical algorithm to calculate the adsorption of
single-site molecules in nanoporous materials using energy grids. The method is about 100 times
faster compared to grand canonical Monte Carlo (GCMC) simulations and is ideal for obtaining quick
estimates of adsorption for high-throughput screening of large databases. Although originally
developed for predicting hydrogen adsorption, the algorithm can be readily applied to other
molecules which can be modeled by a single-site (spherical) such as methane and noble gases. Since
the energy landscape of a material is usually independent of temperature [#f1]_, including thermal
swing into our calculations is also quick and easy. The energy can also be used to visualize the
isoenergy contours (pore surfaces) in a material. Please refer to our documentation page on ReadTheDocs_ for theory, examples and the API reference.

.. image:: https://readthedocs.org/projects/pyisop/badge/?version=latest
    :target: https://pyisop.readthedocs.io/en/latest/?badge=latest&style=for-the-badge
    :alt: Documentation Status

.. image:: https://travis-ci.com/arung-northwestern/pyIsoP.svg?branch=master
    :target: https://travis-ci.com/arung-northwestern/pyIsoP&style=for-the-badge

.. image:: https://badge.fury.io/py/pyIsoP.svg
    :target: https://badge.fury.io/py/pyIsoP


How does it work...?
==========================
Although PyIsoP offers many functionalities, the overall approach can be summarized as shown

.. figure:: ./docs/images/pyisop_doc.png
    :width: 600
    
    
Coming Soon !
=====================
    We are currently working on adding an automated, energy-based, molecular siting module and
    extending the isotherm prediction approach to ethane and higher alkanes. Stay tuned for new features, tests, bug-fixes
    and examples.

.. _ReadTheDocs: https://pyisop.readthedocs.io/en/latest/
.. rubric::Footnotes

.. [#f1] Feynman-Hibbs correction induces a temperature dependency on the energy grid, however this maybe assumed to be weak. For polyatomic probes, the existence of different orientations at any given site also imparts a temperature dependence on the energy grid.


** Acknowledgements: 
    Andrew Rosen, Snurr Research Group, Northwestern Univerisity.
    Project based on the Computational Molecular Science Python Cookiecutter_ version 1.0.

    This work is supported by the U.S. Department of Energy, Office of Basic 
    Energy Sciences, Division of Chemical Sciences, Geosciences and 
    Biosciences through the Nanoporous Materials Genome Center under award 
    DE-FG02-17ER16362.

.. _Cookiecutter: https://github.com/molssi/cookiecutter-cms

Created by: Arun Gopalan
