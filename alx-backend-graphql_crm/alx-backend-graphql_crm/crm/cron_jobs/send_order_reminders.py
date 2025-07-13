# crm/cron_jobs/send_order_reminders.py
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(filename='/tmp/order_reminders_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Set up transport and client
transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=False, retries=3)
client = Client(transport=transport, fetch_schema_from_transport=True)

# Prepare date range for last 7 days
seven_days_ago = (datetime.now() - timedelta(days=7)).date()
query = gql("""
query getRecentOrders {
    allOrders(filter: { orderDateGte: "%s" }) {
        edges {
        node {
            id
            customer {
            email
        }
        }
        }
    }
}
""" % seven_days_ago)

try:
    result = client.execute(query)
    for edge in result["allOrders"]["edges"]:
        order = edge["node"]
        log_entry = f"Order ID: {order['id']} - Customer Email: {order['customer']['email']}"
        logging.info(log_entry)
    print("Order reminders processed!")
except Exception as e:
    logging.error(f"Error retrieving order reminders: {e}")
    print("Failed to process order reminders.")