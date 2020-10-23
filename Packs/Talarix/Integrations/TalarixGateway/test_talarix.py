import demistomock as demisto
import pytest
from Talarix import main, APP
import requests
from unittest.mock import call
import json

TEST_PARAMS = {
    "xsoar_apikey": "testkey",
    "xsoar_server": "https://testserver",
    "url": "https://notreal.com"
}
TEST_INCIDENT = [json.load(open("DATA_TESTINCIDENT.json"))]


def test_main(mocker):
    mocker.patch.object(demisto, 'args', return_value={})
    mocker.patch.object(demisto, 'command', return_value="test-module")
    main()


class MockResponse():
    def json(self):
        return demisto.exampleIncidents[0]['Contents']


def test_route_good_sms(mocker):
    # Path the various objects
    mocker.patch.object(demisto, 'info', return_value="None")
    mocker.patch.object(demisto, 'params', return_value=TEST_PARAMS)
    mocker.patch("requests.post", return_value=MockResponse())

    # Test the SMS receive
    test_client = APP.test_client()
    # First we test a valid incident message

    rv = test_client.post("/", data={
        'txt': "Incident 1234"
    })
    demisto.info.assert_has_calls([call("Received message matching 1234"), call("Updated incident 1234")])


def dtest_upate_table(mocker):
    mocker.patch.object(demisto, 'info', return_value=None)
    mocker.patch.object(demisto, 'params', return_value=TEST_PARAMS)
    mocker.patch.object(demisto, 'incidents', return_value=TEST_INCIDENT)
    mocker.patch.object(demisto, 'executeCommand', return_value=None)
    r = update_sms_table("smstxt", "This is a sent message.")
    assert len(r) == 4
    demisto.executeCommand.assert_called_once()

def test_send_sms(mocker):
    mocker.patch.object(demisto, 'info', return_value="None")
    mocker.patch.object(demisto, 'params', return_value=TEST_PARAMS)
    mocker.patch("requests.post", return_value=MockResponse())


def test_route_bad_sms(mocker):
    # Path the various objects
    mocker.patch.object(demisto, 'info', return_value="None")

    # Test the SMS receive
    test_client = APP.test_client()
    # First we test a valid incident message

    rv = test_client.post("/", data={
        'txt': "Incident"
    })

    demisto.info.assert_called_once_with("Received incoming message with no matching incident.")


## If you want to actually run the WSGI server locally for testing, remove the "don't" and run WSGI as normal.
def dont_test_run_long_running(mocker):
    mocker.patch.object(demisto, 'args', return_value={})
    mocker.patch.object(demisto, 'params', return_value={'longRunningPort': 8000})
    mocker.patch.object(demisto, 'command', return_value="long-running-execution")
    main()
