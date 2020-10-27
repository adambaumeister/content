import demistomock as demisto
import json
from unittest.mock import call

from SendReminderSMS import *

TEST_CONTEXT = {
    "ReminderCount": 0
}

TEST_ARGS = {
    "message": "Test message",
    "number": "+61123456789"
}


def test_first_reminder(mocker):
    """
    Test the case that we've gotten a new message
    """
    mocker.patch.object(demisto, 'args', return_value=TEST_ARGS)
    mocker.patch.object(demisto, 'executeCommand', return_value=TEST_ARGS)

    send_and_update(TEST_CONTEXT)

    calls = [
        call("TalarixSendMessage", {
            "message": TEST_ARGS["message"],
            "number": TEST_ARGS["number"]
        }),
        call("Set", {
            "key": CONTEXT_KEY,
            "value": 1
        })
    ]

    demisto.executeCommand.assert_has_calls(calls)


