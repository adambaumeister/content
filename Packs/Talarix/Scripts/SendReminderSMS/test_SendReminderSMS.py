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

TEST_ARGS_CONTACTS = {
    "message": "Test message",
    "contacts": {
        "domainname": "ITP",
        "managementmobile": "+6122222222",
        "managementname": "Management Contact",
        "primarymobile": "+6111111111",
        "primaryname": "Primary Contact",
        "secondarymobile": "+6133333333",
        "secondaryname": "Secondary Contact"
    }
}


def test_first_reminder_number_only(mocker):
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


def test_first_reminder_contacts(mocker):
    """
    Test the case where we've been given a "Contacts" object
    Should contact the Primary contact only
    """
    mocker.patch.object(demisto, 'args', return_value=TEST_ARGS_CONTACTS)
    mocker.patch.object(demisto, 'executeCommand', return_value=TEST_ARGS)

    send_and_update(TEST_CONTEXT)

    calls = [
        call("TalarixSendMessage", {
            "message": TEST_ARGS["message"],
            "number": "+6111111111"
        }),
        call("Set", {
            "key": CONTEXT_KEY,
            "value": 1
        })
    ]

    demisto.executeCommand.assert_has_calls(calls)


def test_second_reminder_contacts(mocker):
    """
    Test the case where we've been given a "Contacts" object
    Second reminder: Should contact the Primary and Secondary Contacts
    """
    mocker.patch.object(demisto, 'args', return_value=TEST_ARGS_CONTACTS)
    mocker.patch.object(demisto, 'executeCommand', return_value=TEST_ARGS)

    send_and_update({
        "ReminderCount": 1
    })

    calls = [
        call("TalarixSendMessage", {
            "message": TEST_ARGS["message"],
            "number": "+6111111111,+6133333333"
        }),
        call("Set", {
            "key": CONTEXT_KEY,
            "value": 2
        })
    ]

    demisto.executeCommand.assert_has_calls(calls)
