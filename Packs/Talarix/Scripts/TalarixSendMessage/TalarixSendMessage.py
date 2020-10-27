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
    sent_time = d.strftime(("%a, %d %b %Y %H:%M:%S %Z"))

    numbers = argToList(demisto.args().get("number"))
    numbers_str = ",".join(numbers)
    row = {
        "dtm": sent_time,
        "mno": f"sent_{numbers_str}",
        "txt": value,
        "direction": f"Sent to {numbers_str}"
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
    numbers = argToList(demisto.args().get("number"))
    for number in numbers:
        a = {
            "message": message,
            "number": number
        }
        demisto.results(demisto.executeCommand("send_sms", a))
    update_sms_table(table, message)

send_sms()
