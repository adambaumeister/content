import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

''' IMPORTS '''

import requests
from gevent.pywsgi import WSGIServer
from flask import Flask, Response, request
import re
import requests

# Disable insecure warnings
requests.packages.urllib3.disable_warnings()
INTEGRATION_NAME = "Talarix"
''' CONSTANTS '''
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

APP: Flask = Flask('talarix-receiver')

ACKFIELD = demisto.params().get("smsackfield", "smsreceived")
TEXTFIELD = demisto.params().get("smstextfield", "smstext")
APIKEY = demisto.params().get("xsoar_apikey")
SERVER = demisto.params().get("xsoar_server")


class Handler:
    @staticmethod
    def write(msg):
        demisto.info(msg)


DEMISTO_LOGGER: Handler = Handler()


def get_incident(incident_id):
    data = {
        "filter": {
            "query": f"-status:closed -category:job id:{incident_id}"
        }
    }
    headers = {
        "Authorization": APIKEY
    }
    r = requests.post(f"{SERVER}/incidents/search", json=data, headers=headers, verify=False)
    data = r.json()['data']
    if len(data) > 0:
        incident = data[0]
        incident_version = incident['version']
        incident_name = incident['name']
        demisto.results(f"{incident_name} : {incident_version}")
        return incident
    else:
        demisto.results(f"Incident not found")


@APP.route('/', methods=['GET', 'POST'])
def receivesms():
    txt = request.form.get('txt')
    regex_result = re.search(r"(\d+)", txt)
    if regex_result:
        incident_id = regex_result.group(1)
        demisto.info(f"Received message matching {incident_id}")
        try:
            incident = get_incident(incident_id)
            if not incident:
                demisto.info(f"Incident not found or closed:{incident_id}")
                return f"Incident not found or closed:{incident_id}"

            incident['CustomFields'][ACKFIELD] = True
            if TEXTFIELD in incident['CustomFields']:
                incident['CustomFields'][TEXTFIELD].append(request.form)
            else:
                incident['CustomFields'][TEXTFIELD] = [ request.form ]


            demisto.createIncidents([incident])
            demisto.results(f"Updated incident {incident_id}")
            demisto.info(f"Updated incident {incident_id}")
            return "SMS Correctly Received."
        except Exception as e:
            return f"Error processing SMS message:{e}"
    else:
        demisto.info(f"Received incoming message with no matching incident.")
        return "SMS Incorrectly received."



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
        elif command == 'get_incident':
            get_incident(demisto.args().get("incident_id"))
        else:
            readable_output, outputs, raw_response = commands[command](demisto.args(), params)
            return_outputs(readable_output, outputs, raw_response)
    except Exception as e:
        err_msg = f'Error in {INTEGRATION_NAME} Integration [{e}]'
        return_error(err_msg)


if __name__ in ['__main__', '__builtin__', 'builtins']:
    main()
