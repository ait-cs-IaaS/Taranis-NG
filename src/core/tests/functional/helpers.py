class BaseTest:
    base_uri = "/api/v1/"

    def assert_get_ok(self, client, uri, auth_header):
        response = client.get(f"{self.base_uri}/{uri}", headers=auth_header)
        return self.assert_ok(response)

    def assert_post_ok(self, client, uri, json_data, auth_header):
        response = client.post(f"{self.base_uri}/{uri}", json=json_data, headers=auth_header)
        return self.assert_ok(response)

    def assert_post_data_ok(self, client, uri, data, auth_header):
        auth_header["Content-type"] = "multipart/form-data"
        response = client.post(f"{self.base_uri}/{uri}", data=data, headers=auth_header)
        return self.assert_ok(response)

    def assert_get_files_ok(self, client, uri, auth_header):
        response = client.get(f"{self.base_uri}/{uri}", headers=auth_header)
        return self.assert_file_ok(response)

    def assert_put_ok(self, client, uri, auth_header):
        response = client.put(f"{self.base_uri}/{uri}", headers=auth_header)
        return self.assert_ok(response)

    def assert_file_ok(self, response):
        assert response
        assert response.content_type == "text/html; charset=utf-8"
        assert response.data
        assert response.status_code == 200
        return response

    def assert_ok(self, response):
        assert response
        assert response.content_type == "application/json"
        assert response.data
        assert response.status_code == 200
        return response

    def assert_get_failed(self, client, uri):
        response = client.get(f"{self.base_uri}/{uri}")
        assert response
        assert response.content_type == "application/json"
        assert response.get_json()["error"] == "not authorized"
        assert response.status_code == 401
        return response
