#!/usr/bin/env python3
"""
Script to send order reminders for orders within the last 7 days
"""

from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate cutoff date (7 days ago)
cutoff_date = (datetime.now() - timedelta(days=7)).date().isoformat()

# GraphQL query
query = gql("""
query GetRecentOrders($cutoff: Date!) {
  orders(orderDate_Gte: $cutoff) {
    id
    customer {
      email
    }
  }
}
""")

params = {"cutoff": cutoff_date}

# Execute query
result = client.execute(query, variable_values=params)

orders = result.get("orders", [])

# Log to file
with open("/tmp/order_reminders_log.txt", "a") as f:
    for order in orders:
        log_line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Order ID: {order['id']} - Customer Email: {order['customer']['email']}\n"
        f.write(log_line)

print("Order reminders processed!")
