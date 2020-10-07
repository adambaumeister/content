import demistomock as demisto
import pytest
from Talarix import main, APP


def test_main(mocker):
    mocker.patch.object(demisto, 'args', return_value={})
    mocker.patch.object(demisto, 'command', return_value="test-module")
    main()


def test_route_good_sms(mocker):
    # Path the various objects
    mocker.patch.object(demisto, 'info', return_value="None")

    # Test the SMS receive
    test_client = APP.test_client()
    # First we test a valid incident message

    rv = test_client.get("/sms", query_string={
        'txt': "Incident 1234"
    })

    demisto.info.assert_called_once_with("Received message matching 1234")


def test_route_bad_sms(mocker):
    # Path the various objects
    mocker.patch.object(demisto, 'info', return_value="None")

    # Test the SMS receive
    test_client = APP.test_client()
    # First we test a valid incident message

    rv = test_client.get("/sms", query_string={
        'txt': "Incident"
    })

    demisto.info.assert_called_once_with("Received incoming message with no matching incident.")

## If you want to actually run the WSGI server locally for testing, remove the "don't" and run WSGI as normal.
def dont_test_run_long_running(mocker):
    mocker.patch.object(demisto, 'args', return_value={})
    mocker.patch.object(demisto, 'params', return_value={'longRunningPort': 8000})
    mocker.patch.object(demisto, 'command', return_value="long-running-execution")
    main()

