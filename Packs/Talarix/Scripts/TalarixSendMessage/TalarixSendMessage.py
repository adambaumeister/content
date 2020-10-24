import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

''' IMPORTS '''
from datetime import datetime, time, date, timezone, timedelta

def update_sms_table(field, value):
    """
    Add a row to the SMS Text table, usually used by send_sms.
    """
    inc = demisto.incidents()[0]
    if "CustomFields" not in inc:
        return

    if inc['CustomFields'] is None:
        demisto.results("Custom field {} not in incident.".format(field))
        return


    if field not in inc['CustomFields']:
        demisto.results("Custom field {} not in incident.".format(field))
        return

    d = datetime.now()
    sent_time = d.strftime("%d/%m/%y %H:%M:%S")

    row = {
        "dtm": sent_time,
        "mno": "sent_from_xsoar",
        "txt": value
    }
    table = inc['CustomFields'][field]
      
    if not table:
        table = [row]
    elif len(table) == 1 and not table[0]:
        table = [row]
    else:
        table.append(row)
    set_args = {
        field: table
    }
    demisto.results(demisto.executeCommand("setIncident", set_args))
    return table

def send_sms():
    message = demisto.args().get("message")
    table = demisto.args().get("sms_table_field", "smstxt")
    demisto.results(demisto.executeCommand("send_sms", demisto.args()))
    update_sms_table(table, message)

send_sms()
