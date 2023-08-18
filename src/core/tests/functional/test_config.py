import os
import json
from tests.functional.helpers import BaseTest
from werkzeug.datastructures import FileStorage


class TestConfigApi(BaseTest):
    base_uri = "/api/v1/config"

    def test_import_osint_sources(self, client, auth_header, cleanup_sources):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "osint_sources_test_data_v1.json")
        with open(file_path, "rb") as f:
            file_storage = FileStorage(stream=f, filename="osint_sources_test_data_v1.json", content_type="application/json")
            data = {"file": file_storage}
            response = self.assert_post_data_ok(client, "import-osint-sources", data, auth_header)
            assert response.json["count"] == 6
            assert response.json["message"] == "Successfully imported sources"

    def test_export_osint_sources(self, client, auth_header, cleanup_sources):
        response = self.assert_get_ok(client, "export-osint-sources", auth_header)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "osint_sources_test_data_v2.json")
        with open(file_path, "rb") as f:
            assert response.json == json.load(f)

    def test_get_osint_sources(self, client, auth_header, cleanup_sources):
        response = self.assert_get_ok(client, "osint-sources", auth_header)
        totoal_count = response.get_json()["total_count"]
        osint_sources = response.get_json()["items"]

        assert totoal_count > 0
        assert len(osint_sources) > 0

    def test_import_word_lists_json(self, client, auth_header, cleanup_word_lists):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "word_list_test_data.json")
        with open(file_path, "rb") as f:
            file_storage = FileStorage(stream=f, filename="word_list_test_data.json", content_type="application/json")
            data = {"file": file_storage}
            response = self.assert_post_data_ok(client, "import-word-lists", data, auth_header)
            assert response.json["count"] == 1
            assert response.json["message"] == "Successfully imported word lists"

    def test_import_word_lists_csv(self, client, auth_header, cleanup_word_lists):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "word_list_test_data.csv")
        with open(file_path, "rb") as f:
            file_storage = FileStorage(stream=f, filename="word_list_test_data.csv", content_type="text/csv")
            data = {"file": file_storage}
            response = self.assert_post_data_ok(client, "import-word-lists", data, auth_header)
            assert response.json["count"] == 1
            assert response.json["message"] == "Successfully imported word lists"

    def test_export_word_lists(self, client, auth_header, cleanup_word_lists):
        response = self.assert_get_ok(client, "export-word-lists", auth_header)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "word_list_test_data.json")
        with open(file_path, "rb") as f:
            exported_word_lists = response.json
            assert "data" in exported_word_lists
            # Assert that "Test wordlist" is in any of the dicts "name" key
            assert any(d["name"] == "Test wordlist" for d in exported_word_lists["data"])
            assert any(d["name"] == "word_list_test_data.csv" for d in exported_word_lists["data"])

    def test_get_word_lists(self, client, auth_header, cleanup_word_lists):
        response = self.assert_get_ok(client, "word-lists", auth_header)
        totoal_count = response.get_json()["total_count"]
        word_lists = response.get_json()["items"]

        assert totoal_count > 0
        assert len(word_lists) > 0


class TestUserConfigApi(BaseTest):
    base_uri = "/api/v1/config"

    def test_create_user(self, client, auth_header, cleanup_user):
        response = self.assert_post_ok(client, uri="users", json_data=cleanup_user, auth_header=auth_header)
        assert response.json["message"] == "User testuser created"

    def test_modify_user(self, client, auth_header, cleanup_user):
        user_data = {
            "username": "testuser",
            "name": "Testy McTestFace",
        }
        response = self.assert_put_ok(client, uri="users/42", json_data=user_data, auth_header=auth_header)
        assert response.json[0]["message"] == "User 42 updated"

    def test_get_user(self, client, auth_header, cleanup_user):
        response = self.assert_get_ok(client, "users?search=testuser", auth_header)
        assert response.json["total_count"] == 1
        assert response.json["items"][0]["username"] == "testuser"
        assert response.json["items"][0]["name"] == "Testy McTestFace"
        assert "password" not in response.json["items"][0]

    def test_delete_user(self, client, auth_header, cleanup_user):
        response = self.assert_delete_ok(client, uri="users/42", auth_header=auth_header)
        assert response.json[0]["message"] == "User 42 deleted"
