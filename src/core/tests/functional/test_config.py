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

    # def test_get_osint_sources(self, client, auth_header):
    #     response = self.assert_get_ok(client, "/osint-sources", auth_header)
    #     totoal_count = response.get_json()["total_count"]
    #     osint_sources = response.get_json()["items"]

    #     assert totoal_count > 0
    #     assert len(osint_sources) > 0
    #     print(f"Total count: {totoal_count} - osint_sources: {osint_sources}")
