============
UGent Biblio
============

`Ghent University Academic Bibliography`_ contains all the scientific publications by UGent_ Researchers. The API_ is public and pretty straight forward.

To use the API in Python this wrapper is available. Instead of returning JSON, it returns dictionaries, and provides methods for querying the API, instead of having to do the formatting yourself.

Installation
------------

::

    pip install ugentbiblio


Usage
-----


...


Testing
-------
Testing is done with pytest, install it together with some other dependencies

::

    pip install -r requirements_dev.txt

To run all the tests, run

::

    pytest

To run all the tests, except the slow ones, run

::

    py.test -k-slow


.. _`Ghent University Academic Bibliography`: https://biblio.ugent.be/
.. _UGent: http://www.ugent.be
.. _API: https://biblio.ugent.be/doc/api