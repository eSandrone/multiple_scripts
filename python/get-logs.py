import sys
import os
import json
import zipfile
import requests
from requests.auth import HTTPBasicAuth

github_token = "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"
run_id = sys.argv[1]
image = "2"

auth = HTTPBasicAuth("eSandrone", github_token)

headers = {
    "Accept": "application/vnd.github+json"
}

url = "https://api.github.com/repos/eSandrone/multiple_scripts/actions/runs/{}/logs".format(run_id)

response = requests.request(
    "GET",
    url,
    headers=headers,
    auth=auth
)

print(response.content)

open('logs.zip', 'wb').write(response.content)

with zipfile.ZipFile('logs.zip', 'r') as zip:
    zip.extractall()
