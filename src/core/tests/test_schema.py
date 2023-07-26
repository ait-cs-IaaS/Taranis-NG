import schemathesis
import pytest
import re
from hypothesis import settings, Verbosity


@pytest.fixture
def schema_wsgi(app):
    return schemathesis.from_wsgi("/api/v1/doc/swagger.json", app)


schema = schemathesis.from_pytest_fixture("schema_wsgi", validate_schema=True)


@schema.parametrize(endpoint="^/api/v1/analyze")
@settings(verbosity=Verbosity.debug)
def test_analyze(case, auth_header, client):
    response = case.call_wsgi(headers=auth_header)
    case.validate_response(response)


@schema.parametrize(endpoint="^/api/v1/assess")
@settings(verbosity=Verbosity.debug)
def test_assess(case, auth_header, client):
    response = case.call_wsgi(headers=auth_header)
    case.validate_response(response)


@schema.parametrize(endpoint="^/api/v1/assets")
@settings(verbosity=Verbosity.debug)
def test_assets(case, auth_header, client):
    response = case.call_wsgi(headers=auth_header)
    case.validate_response(response)


@schema.parametrize(endpoint="^/api/v1/auth")
@settings(verbosity=Verbosity.debug)
def test_auth(case, client):
    response = case.call_wsgi()
    case.validate_response(response)


@schema.parametrize(endpoint="^/api/v1/bots")
@settings(verbosity=Verbosity.debug)
def test_bots(case, api_header, client):
    response = case.call_wsgi(headers=api_header)
    case.validate_response(response)


@schema.parametrize(endpoint="^/api/v1/collectors")
@settings(verbosity=Verbosity.debug)
def test_collectors(case, api_header, client):
    response = case.call_wsgi(headers=api_header)
    case.validate_response(response)


@schema.parametrize(endpoint="^/api/v1/config")
@settings(verbosity=Verbosity.debug)
def test_config(case, auth_header, client):
    response = case.call_wsgi(headers=auth_header)
    case.validate_response(response)


@schema.parametrize(endpoint="^/api/v1/dashboard")
@settings(verbosity=Verbosity.debug)
def test_dashboard(case, auth_header, client):
    response = case.call_wsgi(headers=auth_header)
    case.validate_response(response)


@schema.parametrize(endpoint="^/api/v1/presenters")
@settings(verbosity=Verbosity.debug)
def test_presenters(case, api_header, client):
    response = case.call_wsgi(headers=api_header)
    case.validate_response(response)


@schema.parametrize(endpoint="^/api/v1/publishers")
@settings(verbosity=Verbosity.debug)
def test_publishers(case, api_header, client):
    response = case.call_wsgi(headers=api_header)
    case.validate_response(response)


@schema.parametrize(endpoint="^/api/v1/worker")
@settings(verbosity=Verbosity.debug)
def test_worker(case, api_header, client):
    response = case.call_wsgi(headers=api_header)
    case.validate_response(response)


# excluded_endpoints = ["analyze", "assess", "assets", "auth", "worker", "bots", "config"]
# excluded_endpoints_regex = f"^(?!/api/v1/{'|/api/v1/'.join(excluded_endpoints)}).*$"


# @schema.parametrize()
# @settings(verbosity=Verbosity.debug)
# def test_schema(case, access_token, client):
#     response = case.call_wsgi(headers={"Authorization": access_token})
#     case.validate_response(response)
