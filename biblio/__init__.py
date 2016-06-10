"""API Connector to the `Ghent University Academic Bibliography`_

All of the calls return (lists) with named tuples.
This means that you can access the data with a.dot.notation instead of the regular["dict"]["notation"].
Note that the API does not return empty values as empty placeholders.

.. code:: python

    publication = single_publication(7175390)

    try:
        print publication.cite.chicago_author_date
    except AttributeError:
        print 'No chicago author date is provided'

.. _`Ghent University Academic Bibliography`: https://biblio.ugent.be/
"""

from .biblio import search, publications_by_organisation, \
    publications_by_project, publications_by_person, publications_by_group, \
    single_publication, BASE_URL

__author__ = 'Stef Bastiaansen'
__email__ = 'stef.bastiaansen@ugent.be'
__copyright__ = 'Copyright (c) 2016 LT3 - UGent'
__license__ = 'Apache License 2.0'
__version__ = '0.2.1'
__url__ = 'https://github.com/megasnort/python-ugent-biblio'
__description__ = 'A Python wrapper around the UGent Biblio API'
