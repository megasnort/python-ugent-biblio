# encoding: utf-8

import requests
import pytest

from biblio.biblio import search, publications_by_person, BASE_URL, NotAllowedParameter, InvalidUGentID


class TestApi:

    # Orphée
    CORRECT_UGENT_ID = 802000574659

    def test_api_exits(self):
        assert 200 == requests.get(BASE_URL + 'publication').status_code

    def test_response_is_json(self):
        assert 'application/json; charset=utf-8' == \
               requests.get(
                   '{}?q=dna&format=json'.format(BASE_URL + 'publication')
               ).headers['content-type']

    def test_search_response_is_a_dict(self):
        assert isinstance(search(q='test'), dict)

    def test_publications_by_person_response_is_a_list(self):
        assert isinstance(publications_by_person(self.CORRECT_UGENT_ID), list)

    def test_search_filters_for_not_allowed_parameters(self):
        with pytest.raises(NotAllowedParameter):
            search(blablobli='test')

    def test_orphee_has_publication(self):
        assert len(publications_by_person(self.CORRECT_UGENT_ID)) > 0

    def test_invalid_ugent_id(self):
        with pytest.raises(InvalidUGentID):
            publications_by_person('lalalalala')