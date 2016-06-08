# encoding: utf-8

"""
.. module:: biblio
   :synopsis: Connector to the `Ghent University Academic Bibliography`_

.. _`Ghent University Academic Bibliography`: https://biblio.ugent.be/
"""


import json
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


def publication(publication_id):
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

    return _get_result(url, {})


def publications_by_person(ugent_id):
    """Get all the publications of a person

    Args:
        ugent_id (int): The numerical ugent_id of the person
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

    return _get_result(url, {})


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

    return _get_result(url, {})


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

    return _get_result(url, {})


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

    return _get_result(url, {})


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

    return _get_result(url, params)


def _get_result(url, params):
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
            return json.loads(response.text)
        except ValueError:
            # some of the api calls return one json object per line
            json_string_list = response.text.split('\n')

            return [json.loads(x) for x in json_string_list if x]

    return None
