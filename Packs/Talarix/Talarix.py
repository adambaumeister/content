import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

''' IMPORTS '''

import requests
from gevent.pywsgi import WSGIServer
from flask import Flask, Response, request
import re

# Disable insecure warnings
requests.packages.urllib3.disable_warnings()
INTEGRATION_NAME = "Talarix"
''' CONSTANTS '''
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

APP: Flask = Flask('talarix-receiver')

ACKFIELD = demisto.params().get("smsackfield", "smsreceived")
TEXTFIELD = demisto.params().get("smstextfield", "smstextfield")


class Handler:
    @staticmethod
    def write(msg):
        demisto.info(msg)


DEMISTO_LOGGER: Handler = Handler()


@APP.route('/sms')
def receivesms():
    txt = request.args.get('txt')
    regex_result = re.search(r"(\d+)", txt)

    if regex_result:
        incident_id = regex_result.group(1)
        demisto.info(f"Received message matching {incident_id}")
        try:
            i = demisto.incidents({"id": incident_id})
            demisto.info(i)

            incident = {
                "id": f"{incident_id}",
                "version": -1,
                "name": "created automatically from long running integration"
            }
            r = demisto.createIncidents([incident])
            demisto.results("Done")
            demisto.info(r)
            return "SMS Correctly Received."
        except Exception as e:
            return f"Error processing SMS message:{e}"
    else:
        demisto.info(f"Received incoming message with no matching incident.")
        return "SMS Incorrectly received."


@APP.route('/')
def ping():
    return "Working!"


def run_long_running(params):
    port = params.get("longRunningPort", 8000)
    port = int(port)
    server = WSGIServer(('0.0.0.0', port), APP, log=DEMISTO_LOGGER)
    server.serve_forever()
    pass


def test_module(dargs, params):
    return "ok", {}, ""


def main():
    """
    Main
    """
    params = demisto.params()

    command = demisto.command()
    demisto.debug('Command being called is {}'.format(command))
    commands = {
        'test-module': test_module,
    }

    try:
        if command == 'long-running-execution':
            run_long_running(params)
        else:
            readable_output, outputs, raw_response = commands[command](demisto.args(), params)
            return_outputs(readable_output, outputs, raw_response)
    except Exception as e:
        err_msg = f'Error in {INTEGRATION_NAME} Integration [{e}]'
        return_error(err_msg)


if __name__ in ['__main__', '__builtin__', 'builtins']:
    main()
