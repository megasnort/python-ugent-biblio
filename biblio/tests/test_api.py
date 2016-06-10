# encoding: utf-8

import requests
import pytest

from biblio.biblio import publications_by_project, publications_by_organisation, search, publications_by_person, \
    publications_by_group, BASE_URL, InvalidID, InvalidYear, single_publication, json_string_to_namedtuple


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
            single_publication('lalalalala')

    def test_publication_invalid_id(self):
        assert single_publication(self.INVALID_PUBLICATION_ID) is None

    def test_publication_has_id(self):
        item = single_publication(self.VALID_PUBLICATION_ID)
        assert item.id
        assert item.id == str(self.VALID_PUBLICATION_ID)

    @pytest.mark.slow
    def test_publications_for_organisation(self):
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

    def test_invalid_ugent_id_should_throw_invalid_year_error(self):
        with pytest.raises(InvalidYear):
            publications_by_organisation('PP10', 'test')

    def test_invalid_ugent_ids_should_throw_invalid_id_error(self):
        with pytest.raises(InvalidID):
            publications_by_group([self.VALID_UGENT_ID, 'oink'])

    def test_json_string_delivers_namedtuple(self):
        string = '[{"kind":"fullText","id":"7175395","access":"private","size":"1124315"}]'
        item = json_string_to_namedtuple(string)

        assert item[0].kind
        assert item[0].id
        assert item[0].access
        assert item[0].size

    def test_id_with_underscore_gets_replaced(self):
        string = '{"kind":"fullText","_id":"7175395","access":"private","size":"1124315"}'
        item = json_string_to_namedtuple(string)
        assert item.id

    def test_id_inlist_with_underscore_gets_replaced(self):
        string = '[{"kind":"fullText","_id":"7175395","access":"private","size":"1124315"}]'
        item = json_string_to_namedtuple(string)

        assert item[0].id

    def test_id_in_dict_in_list_with_underscore_gets_replaced(self):
        string = '{"_lalala":[{"kind":"fullText","_id":"7175395","access":[{"_test": 1, "test2": 2}],"size":"1124315"}, {"_kind":"fullText","_id":"123456","access":"private","size":"1124315"}],"_oink": "4"}'
        item = json_string_to_namedtuple(string)

        assert item.oink
        assert item.lalala[0].id
        assert item.lalala[1].kind

    def test_hyphens_in_fieldnames_get_replace(self):
        string = '{"_lalala":[{"kind":"fullText","_i-d":"7175395","access":[{"_test": 1, "test2": 2}],"siz-e":"1124315"}, {"_kind":"fullText","_id":"123456","access":"private","size":"1124315"}],"_oi-nk": "4"}'
        item = json_string_to_namedtuple(string)

        assert item.oi_nk
        assert item.lalala[0].i_d

    def test_code_in_documentation(self):
        publication = single_publication(7175390)

        if publication.cite.chicago_author_date:
            print(publication.cite.chicago_author_date)
        else:
            print('No chicago author date is provided')
