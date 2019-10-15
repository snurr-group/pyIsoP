================================
Getting Started
================================

Installing PyIsoP
==========================
PyIsoP is deployed on PyPI_ , we can install it easily using pip_ 

.. code-block:: bash

    pip install pyisop
    
.. _pip: https://pypi.org/project/pip/
.. _PyPI: https://pypi.org/

..    conda install -c conda-forge pyisop

.. Tip: Use "--override-channel" option for faster environment resolution.

or clone from github_

.. code-block:: bash

    git clone git@github.com:arung-northwestern/pyIsoP.git
    cd pyIsoP/
    python setup.py install

.. _github: https://github.com/arung-northwestern/pyIsoP

Dependencies
------------------
To use all the functionality of PyIsoP the following python packages are required, which if not present are also installed 
automatically using pip_.

* Python_ 3.6 or newer 
* Numpy_ 1.13.3 or newer
* Scipy_ 1.1.0 or newer
* Sklearn_ 0.19.1 or newer
* ASE_ 3.16.0 recommended (newer versions have trouble reading RASPA generated PDB files).
* PYEVTK_ 1.1.1 or newer
* Pandas_ 0.20.3 or newer
* Numba_ 0.35 or newer
* PyTest_ 5.0.1 or newer
* Dask_ 2.2.0 or newer
* Dask_jobqueue_ 0.6.2 or newer
* Tqdm_ 


.. _Python: https://www.python.org/
.. _Numpy: http://www.numpy.org/
.. _Scipy : https://www.scipy.org/
.. _Sklearn: https://scikit-learn.org/
.. _ASE: https://wiki.fysik.dtu.dk/ase/
.. _PYEVTK: https://bitbucket.org/pauloh/pyevtk
.. _Pandas: https://pandas.pydata.org/
.. _Numba: http://numba.pydata.org/
.. _tqdm: https://github.com/tqdm/tqdm
.. _PyTest: https://docs.pytest.org/en/latest/
.. _Dask: https://dask.org/
.. _Dask_jobqueue: https://jobqueue.dask.org/en/latest/