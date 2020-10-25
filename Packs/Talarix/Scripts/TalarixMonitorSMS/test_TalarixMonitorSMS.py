import demistomock as demisto
import json
from TalarixMonitorSMS import main

TEST_ARGS = {
    "task_id": "stopper",
    "field_id": "smstxt",
    "index": "0"
}

TEST_INCIDENT = [json.load(open("DATA_TESTINCIDENT.json"))]


def test_monitor(mocker):
    """
    Test the case that we've gotten a new message
    """
    mocker.patch.object(demisto, 'args', return_value=TEST_ARGS)
    mocker.patch.object(demisto, 'results', return_value=TEST_ARGS)
    mocker.patch.object(demisto, 'incidents', return_value=TEST_INCIDENT)
    mocker.patch.object(demisto, 'executeCommand', return_value=TEST_ARGS)

    main()
    demisto.executeCommand.assert_called_once()
    demisto.results.assert_called_with("New SMS received!!")


def test_monitor_no_msg(mocker):
    """
    Test the case that where there are no messages at all
    """
    mocker.patch.object(demisto, 'args', return_value=TEST_ARGS)
    mocker.patch.object(demisto, 'results', return_value=TEST_ARGS)
    mocker.patch.object(demisto, 'executeCommand', return_value=TEST_ARGS)

    TEST_INCIDENT[0]['CustomFields'][TEST_ARGS['field_id']] = [{}]
    mocker.patch.object(demisto, 'incidents', return_value=TEST_INCIDENT)
    main()
    demisto.results.assert_called_with("No new sms received.")
    demisto.executeCommand.assert_not_called()


def test_monitor_sent_message_only(mocker):
    """
    Test the case where there is a message, but outgoing only
    """
    mocker.patch.object(demisto, 'args', return_value=TEST_ARGS)
    mocker.patch.object(demisto, 'results', return_value=TEST_ARGS)
    mocker.patch.object(demisto, 'executeCommand', return_value=TEST_ARGS)

    TEST_INCIDENT[0]['CustomFields'][TEST_ARGS['field_id']] = [
        {'dtm': '21/10/2020 05:05:22', 'mno': 'sent_+61123456789', 'txt': 'Blah blah'}]
    mocker.patch.object(demisto, 'incidents', return_value=TEST_INCIDENT)
    main()
    demisto.executeCommand.assert_not_called()
    demisto.results.assert_called_with("No new sms received.")
