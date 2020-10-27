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

    c = 0
    if CONTEXT_KEY in context:
        c = context[CONTEXT_KEY]

    c = c + 1
    message = message.format(c)

    res = demisto.executeCommand("TalarixSendMessage", {
        "message": message,
        "number": demisto.args().get("number")
    })

    demisto.executeCommand("Set", {"key": CONTEXT_KEY, "value": c})
    return res


def main():
    context = get_context()
    demisto.results(send_and_update(context))


if __name__ in ('__builtin__', 'builtins'):
    main()