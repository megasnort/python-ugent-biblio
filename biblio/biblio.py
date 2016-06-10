# encoding: utf-8

"""
API Connector to the Ghent University Academic Bibliography
===========================================================

`Ghent University Academic Bibliography`_ contains all the scientific publications by
UGent_ Researchers. The API_ is public and pretty straight forward.

To use the API in Python this wrapper is available.
Instead of returning plain JSON, it returns named tuples and provides methods for querying the API.

.. note:: Should you consult the original API info, notice two differences

    - Leading underscores on all fields are removed (e.g. ``_id`` becomes ``id``)
    - All hyphens are replaces with underscores (e.g. ``chicago-author-date`` becomes ``chicago_author_date``)


.. _`Ghent University Academic Bibliography`: https://biblio.ugent.be/
.. _UGent: http://www.ugent.be
.. _API: https://biblio.ugent.be/doc/api
"""

import json
from collections import namedtuple

import requests


BASE_URL = 'https://biblio.ugent.be/'


class NotAllowedParameter(Exception):
    """
    Exception placeholder for easier debugging.
    """
    pass


class InvalidID(Exception):
    """
    Exception placeholder for easier debugging.
    """
    pass


class InvalidYear(Exception):
    """
    Exception placeholder for easier debugging.
    """
    pass


def single_publication(publication_id):
    """Get a single publication as a dictionary

    Args:
        publication_id (int): The numerical id, of the wanted publication
    Returns:
        A dictionary if a publication is found,
        None when nothing is found.
    """
    try:
        publication_id = int(publication_id)
    except ValueError:
        raise InvalidID(
            '{0} should be an integer.'
            .format(publication_id)
        )

    url = BASE_URL + 'publication/' + str(publication_id)

    return get_result(url, {})


def publications_by_person(ugent_id):
    """Get all the publications of a person

    Args:
        ugent_id (str): The numerical ugent_id of the person
    Returns:
        A list with dictionaries of all the publications of the given person.
        If no person or publications are found, an empty list is returned.
    """
    try:
        ugent_id_int = int(ugent_id)
    except ValueError:
        raise InvalidID(
            '{0} is an invalid format for a UGentID. It should be an integer.'
            .format(ugent_id)
        )

    url = BASE_URL + 'person/' + str(ugent_id_int) + '/publication/export'

    return get_result(url, {})


def publications_by_organisation(organisation_id, year=None):
    """Get all the publications of an organisation

    Args:
        organisation_id (str): The id of the organisation.
        year (int): The year of publication. When omitted, all the publications are returned
    Returns:
        A list with dictionaries of all the publications of the given organisation.
        If no organisation is found, None is returned.
        If no publication is found, an empty list is returned
    """
    year_prefix = ''

    if year:
        if not str(year).isdigit():
            raise InvalidYear('Year should be an integer')

        year_prefix = '/' + str(year)

    url = BASE_URL + 'organization/' + organisation_id + year_prefix + '/publication/export'

    return get_result(url, {})


def publications_by_group(ugent_ids):
    """Get all the publications of an group of people

    Args:
        ugent_ids (list): A list of integers
    Returns:
        A list with dictionaries of all the publications that
        share the group of people
        If no person or publications are found, an empty list is returned.
    """
    try:
        ugent_ids_int = [int(x) for x in ugent_ids]
    except ValueError:
        raise InvalidID('Not all IDs are valid integers.')

    url = BASE_URL + 'group/' + ','.join([str(x) for x in ugent_ids_int]) + '/publication/export'

    return get_result(url, {})


def publications_by_project(project_id):
    """Get all the publications of a project

    Args:
        project_id (str): The id of the project
    Returns:
        A list with dictionaries of all the publications that
        belong to the given project.
        When no project or publications are found, an empty list is returned.
    """
    url = BASE_URL + 'project/' + project_id + '/publication/export'

    return get_result(url, {})


def search(query=None):
    """Search the Biblio Api for publications having a certain keyword.

    Args:
        query (str): the keyword that needs to be searched
    Returns:
        A list with dictionaries of all the publications that
        match the query
        When no publications are found, an empty list is returned.
    """
    url = BASE_URL + 'publication/export'

    if query:
        params = {'q': query}
    else:
        params = {}

    return get_result(url, params)


def get_result(url, params):
    """Get an API-response, formatted as json back from the API.

    Args:
        url (str): The url that needs to be queried, without get-parameters
    Returns:
        When encountering a status_code other then 200, None is returned.
        If a single json is found, it is returned as a dict.
        If multiple jsons are found, they are returns as dicts in a list.
    """
    params['format'] = 'json'

    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            return json_string_to_namedtuple(response.text)
        except ValueError:
            # some of the api calls return one json object per line
            json_string_list = response.text.split('\n')

            return [json_string_to_namedtuple(x) for x in json_string_list if x]

    return None


def json_string_to_namedtuple(string):
    """

    Args:
        string: a string representing a json that needs to be converted
        to a named tuple

    Returns:
        namedtuple
    """
    return json.loads(
        string,
        object_hook=dictionary_to_namedtuple
    )


def dictionary_to_namedtuple(item):
    """Function used by the object_hook of named_tuple
    to translate a dict to a namedtuple

    Args:
        item (dict): The json object to be converted

    Returns:
        namedtuple: Containing the recursive indexed data of the dict

    """
    for key, value in item.items():  # pylint: disable=unused-variable

        new_key = key

        if '-' in new_key:
            new_key = key.replace('-', '_')
            item[new_key] = item.pop(key)

        if new_key.startswith('_'):
            item[new_key[1:]] = item.pop(new_key)

    return namedtuple('d', item.keys(), rename=False)(*item.values())
