import sys
import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

# CONSTANTS
GITHUB_USER = 'qxz30ra'

# VARIABLES
now = datetime.now().strftime("%H:%M:%S")
github_token = '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'
workflow_id = sys.argv[2] if len(sys.argv) > 2 else 57488918
url = 'https://api.github.com/repos/eSandrone/multiple_scripts/actions/workflows/{}/runs'.format(workflow_id)


# GITHUB CALL
auth = HTTPBasicAuth(GITHUB_USER, github_token)
headers = {
    "Accept": "application/vnd.github+json"
}
response_json = requests.get(url, auth=auth, headers=headers).json()
#sys.stdout.write(json.dumps(response_json['workflow_runs'][0], indent=4))
sys.stdout.write(response_json)
data = response_json['workflow_runs'][0]['run_started_at']
run_started_at = data.replace('T', '').replace('Z', '')
then = datetime.strptime(run_started_at, "%Y-%m-%d%H:%M:%S")
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d%H:%M:%S")
parsed_datetime = datetime.strptime(formatted_datetime, "%Y-%m-%d%H:%M:%S")
to_execute = "true" if (parsed_datetime - then).total_seconds()/3600 > 23 else "false"
sys.stdout.write(to_execute)
