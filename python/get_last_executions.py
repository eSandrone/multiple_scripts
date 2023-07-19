import sys
import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime


# TOKEN NON FUNZIONANTE (al momento nello script ma sarà un parametro di ingresso)
# Per test in locale delle funzioni non è necessario il token (commentare righe 35-36-37-59-60-61 e togliere il commento a righe 38-62-63-65 per eseguire lo script)
# Per testare get_webhook_for_team() commmentare riga 99 e togliere il commento da riga 100
# NB Per avviare lo script sono necessari i primi tre input (github_token, workflow_id e only_last_execution) anche se non verrano utilizzati in locale
# Dettagli in fondo al file

# CONSTANTS
RESPONSE_JSON_MOCK = '../.github/mocks/response.json'
TEAMS_DATA_FILE = '../.github/variables/teams.json'
GITHUB_USER = 'qxz30ra'
GITHUB_API_BASE_URL = 'https://api.github.com/repos/eSandrone/multiple_scripts/actions'
GITHUB_API_GET_HEADERS = {
        "Accept": "application/vnd.github+json"
    }

# VARIABLES
now = datetime.now().strftime("%H:%M:%S")

# GITHUB CALL
def get_workflow_executions(token: str, id: int, only_last_execution: str, hours: int):
    """ Permette di recuperare tutte le esecuzioni di un dato workflow
    Se il parametro 'only_last_execution' è True, questa funzione si comporta come lo script get_last_workflow_execution.py già presente
    altrimenti recupera tutti gli id delle esecuzioni avvenute entro il valore di 'hours' (di default 23)
    Successivamente vengono fatte n chiamate tramite webhook per mandare messaggio su teams (da modificare file teams.json per farlo funzionare correttamente)
    Possibile modifica: far mandare la notifica direttamente da questo script (già fatto)
    NB Inserire nel file teams.json anche il webhook del canale per ogni team (da richiedere)
    """
    url = '{}/workflows/{}/runs'.format(GITHUB_API_BASE_URL, id)
    auth = HTTPBasicAuth(GITHUB_USER, token)
    response_json = get_call_github_api(url, auth)
    # response_json = json.loads(open(RESPONSE_JSON_MOCK, 'r').read())
    workflow_ids: list = []
    data = response_json['workflow_runs']
    for run in data:
        run_started_at = run['run_started_at'].replace('T', '').replace('Z', '')
        then = datetime.strptime(run_started_at, "%Y-%m-%d%H:%M:%S")
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d%H:%M:%S")
        parsed_datetime = datetime.strptime(formatted_datetime, "%Y-%m-%d%H:%M:%S")
        get_last = True if only_last_execution.__eq__('True') else False
        if get_last:
            execute_tests = "true" if (parsed_datetime - then).total_seconds()/3600 > int(hours) else "false"
            sys.stdout.write(execute_tests)
            break
        was_executed = True if (parsed_datetime - then).total_seconds()/3600 < int(hours) else False
        if was_executed is not True:
            break
        workflow_ids.append(run['id'])
    # Da modificare righe 60-61 in base a come sceglieremo di chiamare lo step
    for id in workflow_ids:
        url = '{}/runs/{}/jobs'.format(GITHUB_API_BASE_URL, id)
        job_name = get_call_github_api(url, auth)['jobs'][0]['steps'][2]['name']
        repository_name = job_name[job_name.index('Print')+len('Print '):]
        team = job_name[job_name.index('Print'):len('Print')]
        # repository_name = 'TEST REPOSITORY NAME'
        # team = 'Test team name'
        webhook = get_webhook_for_team(team)
        # send_message_to_teams(repository_name, team, webhook, hours)

# UTILS
def get_call_github_api(url: str, auth: HTTPBasicAuth):
    return requests.get(url, auth=auth, headers=GITHUB_API_GET_HEADERS).json()

def send_message_to_teams(repository_name: str, team: str, webhook: str, hours: int):
    url = webhook
    call_payload = {
        "text": "Hello @{}, a dangerous dependency was found by the WIZ tool in the PIP instance that run the tests.\nIn the last {} hours the test present in the repository {} have been performed.\nThis repository may contain a dependecy with severity CRITICAL or HIGH!".format(team, hours, repository_name)
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.request(
        'POST',
        f'{url}',
        headers=headers,
        data=json.dumps(call_payload).encode('utf-8')
    )
    print(response.status_code)

def get_webhook_for_team(team: str):
    pip_supported_teams = json.loads(open(TEAMS_DATA_FILE, 'r').read())
    return pip_supported_teams[team.capitalize()]['webhook']

if __name__ == '__main__':
    github_token = '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' # Token classico di GitHub per autenticazione
    workflow_id = sys.argv[2] # l'ID del workflow per recuperare le sue esecuzioni passate
    only_last_execution = sys.argv[3] # I valori possono essere True o False
    hours = sys.argv[4] if len(sys.argv) > 4 else 23 # Indica entro quante ore devono essere stati eseguiti i test (PER WIZ)
    get_workflow_executions(github_token, workflow_id, only_last_execution, hours)
    # get_webhook_for_team('Zulu')
