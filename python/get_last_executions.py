import sys
import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

# CONSTANTS
GITHUB_USER = 'qxz30ra'
GITHUB_API_BASE_URL = 'https://api.github.com/repos/eSandrone/multiple_scripts/actions'
GITHUB_API_GET_HEADERS = {
        "Accept": "application/vnd.github+json"
    }

# VARIABLES
now = datetime.now().strftime("%H:%M:%S")

# GITHUB CALL
def get_workflow_executions(token: str, id: int, only_last_execution: str, hours: int):
    url = '{}/workflows/{}/runs'.format(GITHUB_API_BASE_URL, id)
    auth = HTTPBasicAuth(GITHUB_USER, token)
    response_json = get_call_github_api(url, auth)
    workflow_ids: list = []
    data = response_json['workflow_runs']
    for run in data:
        run_started_at = run['run_started_at'].replace('T', '').replace('Z', '')
        then = datetime.strptime(run_started_at, "%Y-%m-%d%H:%M:%S")
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d%H:%M:%S")
        parsed_datetime = datetime.strptime(formatted_datetime, "%Y-%m-%d%H:%M:%S")
        get_one = True if only_last_execution.__eq__('True') else False
        if get_one:
            to_execute = "true" if (parsed_datetime - then).total_seconds()/3600 > int(hours) else "false"
            sys.stdout.write(to_execute)
            break
        was_executed = True if (parsed_datetime - then).total_seconds()/3600 < int(hours) else False
        if was_executed is not True:
            break
        workflow_ids.append(run['id'])
    print(workflow_ids)
    for id in workflow_ids:
        url = '{}/runs/{}/jobs'.format(GITHUB_API_BASE_URL, id)
        job_name = get_call_github_api(url, auth)['jobs'][0]['steps'][2]['name']
        repository_name = job_name[job_name.index('Print')+len('Print '):]
        team = job_name[job_name.index('Print'):len('Print')]
        print(repository_name, '\n', team)
        # sendMessageToMSTeams(repository_name, team ,auth)

# UTILS
def get_call_github_api(url: str, auth: HTTPBasicAuth):
    return requests.get(url, auth=auth, headers=GITHUB_API_GET_HEADERS).json()

def sendMessageToMSTeams(repository_name: str, team: str, auth: HTTPBasicAuth):
    url = '{}/dispatches'.format(GITHUB_API_BASE_URL)
    call_payload = {
        "event_type": "curl",
        "client_payload": {
            "text": "Dangerous dependency found by the WIZ tool in the instance running the tests. Repository {} may contain a dependecy with severity CRITICAL or HIGH!".format(repository_name),
            "team": team
        }
    }
    headers = {
        "Accept": "application/vnd.github+json"
    }
    response = requests.request(
        "POST",
        url,
        auth=auth,
        headers=headers,
        data=json.dumps(call_payload)
    )


if __name__ == '__main__':
    github_token = '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'
    workflow_id = sys.argv[2]
    only_last_execution = sys.argv[3]
    hours = sys.argv[4] if len(sys.argv) > 4 else 23
    get_workflow_executions(github_token, workflow_id, only_last_execution, hours)
