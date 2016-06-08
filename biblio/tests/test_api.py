# encoding: utf-8

import requests
import pytest

from biblio.biblio import publications_by_project, publications_by_organisation, search, publications_by_person, \
    publications_by_group, BASE_URL, InvalidID, publication


class TestApi:
    # Orphée
    VALID_UGENT_ID = '802000574659'
    VALID_PUBLICATION_ID = '5731482'

    # Orphée and Veronique
    VALID_UGENT_GROUP = ['802000574659', '802000247889']

    # Department of Experimental psychology
    VALID_ORGANISATION_ID = 'PP02'

    # LT3
    VALID_PROJECT_ID = 'LT3'

    INVALID_UGENT_ID = '1'
    INVALID_PUBLICATION_ID = '1'

    def test_valid_response(self):
        response = requests.get(
            BASE_URL + 'publication/' + self.VALID_PUBLICATION_ID, {'q': 'test', 'format': 'json'}
        )

        assert 200 == response.status_code
        assert 'application/json; charset=utf-8' == response.headers['content-type']

    def test_search_response_is_a_list(self):
        assert isinstance(search('111'), list)

    @pytest.mark.slow
    def test_search_without_an_argument_returns_everything(self):
        assert len(search()) > 100

    def test_publications_by_person_response_is_a_list(self):
        assert isinstance(publications_by_person(self.VALID_UGENT_ID), list)

    def test_publications_by_invalid_person_response_is_empty_list(self):
        assert len(publications_by_person(self.INVALID_UGENT_ID)) == 0

    def test_orphee_has_publication(self):
        assert len(publications_by_person(self.VALID_UGENT_ID)) > 0

    def test_publications_by_persons_response_is_a_list(self):
        assert isinstance(publications_by_group(self.VALID_UGENT_GROUP), list)

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

    @pytest.mark.slow
    def test_publication_for_organisations(self):
        all_items = publications_by_organisation(self.VALID_ORGANISATION_ID)
        items_for_year = publications_by_organisation(self.VALID_ORGANISATION_ID, 2015)
        assert isinstance(all_items, list)
        assert len(all_items) > 10
        assert len(items_for_year) > 1
        assert len(all_items) > len(items_for_year)

    def test_publication_for_project(self):
        items = publications_by_project(self.VALID_PROJECT_ID)
        assert isinstance(items, list)
        assert len(items) > 10
