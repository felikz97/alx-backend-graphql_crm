# crm/tasks.py
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

@shared_task
def generate_crm_report():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        client = Client(transport=RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=False, retries=3), fetch_schema_from_transport=True)
        query = gql("""
        {
            allCustomers {
                edges { node { id } }
            }
            allOrders {
                edges {
                node {
                    id
                    totalAmount
                }
                }
            }
        }
        """)
        result = client.execute(query)
        total_customers = len(result['allCustomers']['edges'])
        orders = result['allOrders']['edges']
        total_orders = len(orders)
        total_revenue = sum(float(order['node']['totalAmount']) for order in orders)
        report = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, ${total_revenue:.2f} revenue"
    except Exception as e:
        report = f"{timestamp} - Error generating report: {e}"

    with open('/tmp/crm_report_log.txt', 'a') as f:
        f.write(report + "\n")