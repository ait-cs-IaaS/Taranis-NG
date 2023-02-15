from core.model.news_item import NewsItemAggregate

class TestAssessApi(object):

    def _cleanup(self, dbsession):
        # Clean Up the mess
        dbsession.delete(os)
        dbsession.delete(ni)
        dbsession.delete(nv)
        dbsession.delete(nia)
        dbsession.delete(na)
        dbsession.commit()


    def teardown_class(self):
        print("teardown test")

    def test_get_OSINTSourceGroupsAssess_auth(self, client, auth_header):
        """
        This test queries the OSINTSourceGroupsAssess authenticated.
        It expects a valid data and a valid status-code
        """
        response = client.get("/api/v1/assess/osint-source-groups", headers=auth_header)
        assert response
        assert response.content_type == "application/json"
        assert response.data
        assert response.status_code == 200

    def test_get_OSINTSourceGroupsAssess_unauth(self, client):
        """
        This test queries the OSINTSourceGroupsAssess UNauthenticated.
        It expects "not authorized"
        """
        response = client.get("/api/v1/assess/osint-source-groups")
        assert response
        assert response.content_type == "application/json"
        assert response.get_json()["error"] == "not authorized"
        assert response.status_code == 401

    def test_get_OSINTSourceGroupsList_auth(self, client, auth_header):
        """
        This test queries the OSINTSourceGroupsList authenticated.
        It expects a valid data and a valid status-code
        """
        response = client.get("/api/v1/assess/osint-source-group-list", headers=auth_header)
        assert response
        assert response.content_type == "application/json"
        assert response.data
        assert response.status_code == 200

    def test_get_OSINTSourceGroupsList_unauth(self, client):
        """
        This test queries the OSINTSourceGroupsList UNauthenticated.
        It expects "not authorized"
        """
        response = client.get("/api/v1/assess/osint-source-group-list")
        assert response
        assert response.content_type == "application/json"
        assert response.get_json()["error"] == "not authorized"
        assert response.status_code == 401

    def test_get_OSINTSourcesList_auth(self, client, auth_header):
        """
        This test queries the OSINTSourcesList authenticated.
        It expects a valid data and a valid status-code
        """
        response = client.get("/api/v1/assess/osint-sources-list", headers=auth_header)
        assert response
        assert response.content_type == "application/json"
        assert response.data
        assert response.status_code == 200

    def test_get_OSINTSourcesList_unauth(self, client):
        """
        This test queries the OSINTSourcesList UNauthenticated.
        It expects "not authorized"
        """
        response = client.get("/api/v1/assess/osint-sources-list")
        assert response
        assert response.content_type == "application/json"
        assert response.get_json()["error"] == "not authorized"
        assert response.status_code == 401

    def test_get_ManualOSINTSources_auth(self, client, auth_header):
        """
        This test queries the ManualOSINTSources authenticated.
        It expects a valid data and a valid status-code
        """
        response = client.get("/api/v1/assess/manual-osint-sources", headers=auth_header)
        assert response
        assert response.content_type == "application/json"
        assert response.data
        assert response.status_code == 200

    def test_get_ManualOSINTSources_unauth(self, client):
        """
        This test queries the ManualOSINTSources UNauthenticated.
        It expects "not authorized"
        """
        response = client.get("/api/v1/assess/manual-osint-sources")
        assert response
        assert response.content_type == "application/json"
        assert response.get_json()["error"] == "not authorized"
        assert response.status_code == 401

    def test_post_AddNewsItem_auth(self, client, news_item_data, dbsession, auth_header):
        """
        This test queries the AddNewsItem authenticated.
        It expects a valid data and a valid status-code
        """
        attribs = {
                "key": "1293",
                "value": "some value",
                "binary_mime_type": "dGVzdAo=",
                "binary_value": "dGVzdAo="
        }

        news_item = {
                "id": "1337",
                "title": "test title",
                "review": "test review",
                "source": "test source",
                "link": "https://linky.link.lnk",
                "hash": "test hash",
                "published": "yes",
                "author": "James Bond",
                "content": "Diamonds are forever",
                "collected": "26.01.2023 - 16:36",
                "attributes": [attribs]
        }
        before = news_item_data.count_all()
        response = client.post("/api/v1/assess/news-items", json=news_item, headers=auth_header)
        assert response
        assert response.content_type == "application/json"
        assert response.data
        assert response.status_code == 200
        assert before < news_item_data.count_all()
        # cleanup
        ni = news_item_data.query.filter_by(id="1337").one()
        dbsession.delete(ni)
        dbsession.commit()

    def test_post_AddNewsItem_unauth(self, client, news_item_data, dbsession):
        """
        This test queries the AddNewsItem UNauthenticated.
        It expects "not authorized"
        """
        attribs = {
                "key": "1293",
                "value": "some value",
                "binary_mime_type": "dGVzdAo=",
                "binary_value": "dGVzdAo="
        }

        news_item = {
                "id": "1337",
                "title": "test title",
                "review": "test review",
                "source": "test source",
                "link": "https://linky.link.lnk",
                "hash": "test hash",
                "published": "yes",
                "author": "James Bond",
                "content": "Diamonds are forever",
                "collected": "26.01.2023 - 16:36",
                "attributes": [attribs]
        }
        before = news_item_data.count_all()
        response = client.post("/api/v1/assess/news-items", json=news_item)
        assert response
        assert response.content_type == "application/json"
        assert response.get_json()["error"] == "not authorized"
        assert response.status_code == 401
        assert before == news_item_data.count_all()

    def test_get_NewsItemAggregates_auth(self, client, news_item, dbsession, auth_header):
        """
        This test queries the NewsItemAggregates authenticated.
        It expects a valid data and a valid status-code
        """

        from core.model.news_item import NewsItemAggregate, NewNewsItemDataSchema
        from core.model.osint_source import OSINTSource
        from shared.schema.osint_source import OSINTSourceExportSchema

        ossi = {
          "description": "",
          "name": "BSI Bund",
          "parameter_values": [
            {
              "value": "https://www.bsi.bund.de/SiteGlobals/Functions/RSSFeed/RSSNewsfeed/RSSNewsfeed.xml",
              "parameter": {
                "key": "FEED_URL"
              }
            },
          ],
          "collector": {
            "type": "RSS_COLLECTOR"
          }
        }

        osint_source = OSINTSourceExportSchema().load(ossi)
        OSINTSource.import_new(osint_source)
        os = OSINTSource.get_all()[0]

        news_items_data_list = [
          {
            "id": "1be00eef-6ade-4818-acfc-25029531a9a5",
            "content": "TEST CONTENT YYYY",
            "source": "https: //www.bsi.bund.de/SiteGlobals/Functions/RSSFeed/RSSNewsfeed/RSSNewsfeed.xml",
            "title": "Mobile World Congress 2023",
            "author": "",
            "collected": "26.01.2023 - 16:36",
            "hash": "82e6e99403686a1072d0fb2013901b843a6725ba8ac4266270f62b7614ec1adf",
            "attributes": [],
            "review": "",
            "link": "https://www.bsi.bund.de/SharedDocs/Termine/DE/2023/MWC_2023.html",
            "osint_source_id": os.id,
            "published": "2023-02-13T00: 00: 00+01: 00"
          },
          {
            "id": "0a129597-592d-45cb-9a80-3218108b29a0",
            "content": "TEST CONTENT XXXX",
            "source": "https: //www.bsi.bund.de/SiteGlobals/Functions/RSSFeed/RSSNewsfeed/RSSNewsfeed.xml",
            "title": "Bundesinnenministerin Nancy Faeser wird Claudia Plattner zur neuen BSI-Präsidentin berufen",
            "author": "",
            "collected": "26.01.2023 - 16:36",
            "hash": "e270c3a7d87051dea6c3dc14234451f884b427c32791862dacdd7a3e3d318da6",
            "attributes": [],
            "review": "Claudia Plattner wird ab 1. Juli 2023 das Bundesamt für Sicherheitin der Informationstechnik (BSI) leiten.",
            "link": "https: //www.bsi.bund.de/DE/Service-Navi/Presse/Alle-Meldungen-News/Meldungen/BSI-Praesidentin_230207.html",
            "osint_source_id": os.id,
            "published": "2023-02-07T09:15:00+01:00"
          }
        ]

        news_item_data_schema = NewNewsItemDataSchema(many=True)
        news_items_data = news_item_data_schema.load(news_items_data_list)
        nia = NewsItemAggregate()

        for nid in news_items_data:
            nia.create_new_for_all_groups(nid)

        response = client.get("/api/v1/assess/news-item-aggregates", headers=auth_header)
        assert response
        assert response.data
        assert response.get_json()["total_count"] > 0
        assert response.content_type == "application/json"
        assert response.status_code == 200

        response = client.get("/api/v1/assess/news-item-aggregates?search=notexistent", headers=auth_header)
        assert response.get_json()["total_count"] == 0

        response = client.get("/api/v1/assess/news-item-aggregates?notexistent=notexist", headers=auth_header)
        assert response.get_json()["total_count"] > 0

        response = client.get("/api/v1/assess/news-item-aggregates?read=1", headers=auth_header)
        assert response.get_json()["total_count"] > 0

        response = client.get("/api/v1/assess/news-item-aggregates?relevant", headers=auth_header)
        assert response.get_json()["total_count"] > 0

        response = client.get("/api/v1/assess/news-item-aggregates?in_report=true", headers=auth_header)
        assert response.get_json()["total_count"] > 0

        response = client.get("/api/v1/assess/news-item-aggregates?range=20", headers=auth_header)
        assert response.get_json()["total_count"] == 0

        response = client.get("/api/v1/assess/news-item-aggregates?sort=20", headers=auth_header)
        assert response.get_json()["total_count"] > 0

        response = client.get("/api/v1/assess/news-item-aggregates?offset=1", headers=auth_header)
        assert response.get_json()["total_count"] > 0

        response = client.get("/api/v1/assess/news-item-aggregates?limit=-1", headers=auth_header)
        assert response.get_json()["total_count"] > 0



