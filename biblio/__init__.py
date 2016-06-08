"""Connector to the `Ghent University Academic Bibliography`_

.. _`Ghent University Academic Bibliography`: https://biblio.ugent.be/
"""

from .biblio import search, publications_by_organisation, \
    publications_by_project, publications_by_person, publications_by_group, \
    publication, BASE_URL

__author__ = 'Stef Bastiaansen'
__email__ = 'stef.bastiaansen@ugent.be'
__copyright__ = 'Copyright (c) 2016 LT3 - UGent'
__license__ = 'Apache License 2.0'
__version__ = '0.1.1'
__url__ = 'https://github.com/megasnort/python-ugent-biblio'
__description__ = 'A Python wrapper around the UGent Biblio API'
