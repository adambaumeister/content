import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

from_time = demisto.args().get("from")
to_time = demisto.args().get("to")

MAX_GRAPH = 10

query_params = {
    "query": "-closed",
    "fromDate": from_time,
    "toDate": to_time
}

incidents_query_res = demisto.executeCommand('GetIncidentsByQuery', query_params)
incidents = json.loads(incidents_query_res[-1]['Contents'])
incidents_by_name = {}
for incident in incidents:
    incidents_by_name.setdefault(incident["name"], []).append(incident)

results = []
for name in sorted(incidents_by_name, key=lambda k: len(incidents_by_name[k]), reverse=True):
    r = {
        "name": name,
        "data": [len(incidents_by_name[name])],
    }
    results.append(r)

# If there are more than the provided MAX_GRAPH results, trim so we get the Top 10 and then add an "others" column
if len(results) > MAX_GRAPH:
    others = results[MAX_GRAPH:]
    results = results[:MAX_GRAPH]
    r = {
        "name": "others",
        "data": [len(others)],
    }
    results.append(r)

demisto.results(json.dumps(results))