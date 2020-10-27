import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *
task_tag = demisto.args().get("task_tag")

demisto.executeCommand("taskComplete", {"id":task_tag})
inc = demisto.incident()
smstxt = inc['CustomFields']['smstxt']

now = datetime.now()
dt_string = now.strftime("%a, %d %b %Y %H:%M:%S %Z")

if not smstxt[0]:
    smstxt = {
        "dtm": dt_string,
        "mno": demisto.args().get("ack_mobileNo"),
        "txt": demisto.args().get("ack_SMS_message"),
        "direction": demisto.args().get("ack_mobileNo")
    }
else :
    smstxt.append({
            "dtm": dt_string,
            "mno": demisto.args().get("ack_mobileNo"),
            "txt": demisto.args().get("ack_SMS_message"),
            "direction": demisto.args().get("ack_mobileNo")
    })

a = { "smstxt": smstxt }
demisto.results(demisto.executeCommand("setIncident", a))
