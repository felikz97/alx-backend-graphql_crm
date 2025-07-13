# crm/cron.py
from datetime import datetime
import requests

def log_crm_heartbeat():
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{timestamp} CRM is alive"
    try:
        response = requests.post('http://localhost:8000/graphql', json={'query': '{ hello }'})
        if response.status_code == 200 and 'data' in response.json():
            message += " - GraphQL OK"
        else:
            message += " - GraphQL failed"
    except Exception as e:
        message += f" - GraphQL error: {e}"

    with open('/tmp/crm_heartbeat_log.txt', 'a') as log:
        log.write(message + "\n")
        