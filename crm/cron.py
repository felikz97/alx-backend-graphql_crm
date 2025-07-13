# crm/cron.py
from gql.transport.requests import RequestsHTTPTransport 
from gql import gql, Client
from datetime import datetime
import requests

# Set up transport and client for GraphQL requests
transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=False, retries=3)
client = Client(transport=transport, auto_schema=True)

def log_crm_heartbeat():
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{timestamp} CRM is alive"
    try:
        response = client.execute(gql('{ hello }'))
        if response and 'data' in response:
            message += " - GraphQL OK"
        else:
            message += " - GraphQL failed"
    except Exception as e:
        message += f" - GraphQL error: {e}"

    with open('/tmp/crm_heartbeat_log.txt', 'a') as log:
        log.write(message + "\n")

def update_low_stock():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        response = requests.post('http://localhost:8000/graphql', json={
            'query': 'mutation { updateLowStockProducts { products { name stock } message } }'
        })
        if response.status_code == 200:
            data = response.json()
            lines = [f"{timestamp} - {p['name']} restocked to {p['stock']}" for p in data['data']['updateLowStockProducts']['products']]
            with open('/tmp/low_stock_updates_log.txt', 'a') as f:
                f.write("\n".join(lines) + "\n")
        else:
            raise Exception("Bad response")
    except Exception as e:
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(f"{timestamp} - Error: {e}\n")
    print("Low stock update processed!")
    return "Low stock update processed!"