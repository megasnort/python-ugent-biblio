# encoding: utf-8

import requests
import pytest

from biblio.biblio import search, publications_by_person, BASE_URL, NotAllowedParameter, InvalidID, publication


class TestApi:
    # Orphée
    VALID_UGENT_ID = 802000574659
    VALID_PUBLICATION_ID = 5731482

    INVALID_UGENT_ID = 1
    INVALID_PUBLICATION_ID = 1

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
        assert isinstance(publications_by_person(self.VALID_UGENT_ID), list)

    def test_publications_by_invalid_person_response_is_empty_list(self):
        assert len(publications_by_person(self.INVALID_UGENT_ID)) == 0

    def test_search_filters_for_not_allowed_parameters(self):
        with pytest.raises(NotAllowedParameter):
            search(blablobli='test')

    def test_orphee_has_publication(self):
        assert len(publications_by_person(self.VALID_UGENT_ID)) > 0

    def test_invalid_ugent_id(self):
        with pytest.raises(InvalidID):
            publications_by_person('lalalalala')

    def test_invalid_publication_id(self):
        with pytest.raises(InvalidID):
            publication('lalalalala')

    def test_publication_invalid_id(self):
        assert publication(self.INVALID_PUBLICATION_ID) is None

    def test_publication_has_id(self):
        item = publication(self.VALID_PUBLICATION_ID)
        assert '_id' in item
        assert item['_id'] == str(self.VALID_PUBLICATION_ID)


