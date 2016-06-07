# encoding: utf-8

"""
Ghent University Academic Bibliography (https://biblio.ugent.be) contains
all the scientific publications by [UGent](http://www.ugent.be) Researchers.
The API (https://biblio.ugent.be/doc/api) is public and pretty straight forward.

To use the API in Python this wrapper is available.
Instead of returning JSON, it returns dictionaries and lists,
and provides methods for querying the API,
instead of having to do the formatting yourself.
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


def publication(publication_id):
    """
    Return a single publication
    :param publication_id:
    :return:
    """
    try:
        publication_id = int(publication_id)
    except ValueError:
        raise InvalidID(
            '{0} should be an integer.'
            .format(publication_id)
        )

    url = BASE_URL + 'publication/' + str(publication_id)

    return _get_result(url, None)


def publications_by_person(ugent_id):
    """
    Return all the publications of certain ugent id
    :param ugent_id:
    :return:
    """
    try:
        ugent_id_int = int(ugent_id)
    except ValueError:
        raise InvalidID(
            '{0} is an invalid format for a UGentID.'
            .format(ugent_id)
        )

    url = BASE_URL + 'person/' + str(ugent_id_int) + '/publication/export'

    return _get_result(url, None)


def search(**kwargs):
    """
    Search the Biblio-Api for publications have a certain keyword
    :param kwargs:
    :return:
    """
    allowed_parameters = ('q', 'sort')
    url = BASE_URL + 'publication'

    return _get_result(url, allowed_parameters, **kwargs)


def _get_result(url, allowed_parameters, **kwargs):
    """
    Get an API-response, formatted as json back from the API.

    :param url:
    :param allowed_parameters:
    :param kwargs:
    :return:
    """
    if allowed_parameters:
        for arg in kwargs:
            if arg not in allowed_parameters:
                raise NotAllowedParameter(
                    '{0} is not allowed as parameter. Only {1} are allowed.'
                    .format(arg, ','.join(allowed_parameters))
                )

    kwargs['format'] = 'json'

    response = requests.get(url, params=kwargs)

    if response.status_code == 200:
        try:
            return json.loads(response.text)
        except ValueError:
            # some of the api calls return one json object per line
            json_string_list = response.text.split('\n')

            return [json.loads(x) for x in json_string_list if x]

    return None


