import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *


def monitor_table(task_id, field_id, index):
    inc = demisto.incidents()[0]

    if field_id in inc["CustomFields"]:
        table = inc["CustomFields"][field_id]
        rcv_sms = []
        for row in table:
            if 'mno' in row:
                if "sent" not in row['mno']:
                    rcv_sms.append(row)

        current_length = len(rcv_sms)
        if current_length == index:
            demisto.results("No new sms received.")
        elif current_length > index:
            demisto.executeCommand("taskComplete", {"id": task_id})
            demisto.results("New SMS received!!")
        else:
            demisto.results("Invalid index provided.")


def main():
    task_id = demisto.args().get("task_id")
    field_id = demisto.args().get("field_id")
    index = demisto.args().get("index")
    index = int(index)
    monitor_table(task_id, field_id, index)


if __name__ in ('__builtin__', 'builtins'):
    main()
