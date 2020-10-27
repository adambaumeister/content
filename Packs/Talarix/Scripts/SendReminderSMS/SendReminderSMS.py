import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

''' IMPORTS '''
CONTEXT_KEY = "ReminderCount"


def get_context():
    inc = demisto.incidents()[0]
    res = demisto.executeCommand("getContext", {"id": inc["id"]})
    try:
        return res[0]['Contents'].get('context') or {}
    except Exception:
        return {}


def send_and_update(context):
    message = demisto.args().get("message")
    number = demisto.args().get("number")
    contacts = argToList(demisto.args().get("contacts"))

    c = 0
    if CONTEXT_KEY in context:
        c = context[CONTEXT_KEY]

    if contacts:
        contacts = contacts[0]
        if c == 0:
            number = contacts["primarymobile"]
        elif c >= 1:
            number = "{},{}".format(contacts['primarymobile'],contacts['secondarymobile'])

    c = c + 1
    message = message.format(c)

    res = demisto.executeCommand("TalarixSendMessage", {
        "message": message,
        "number": number
    })

    demisto.executeCommand("Set", {"key": CONTEXT_KEY, "value": c})
    return res


def main():
    context = get_context()
    demisto.results(send_and_update(context))


if __name__ in ('__builtin__', 'builtins'):
    main()