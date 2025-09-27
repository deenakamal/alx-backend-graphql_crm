from celery import shared_task
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import requests

@shared_task
def generate_crm_report():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{now} - Report: "

    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql(
            """
            query {
                totalCustomers
                totalOrders
                totalRevenue
            }
            """
        )

        result = client.execute(query)
        customers = result["totalCustomers"]
        orders = result["totalOrders"]
        revenue = result["totalRevenue"]

        log_message += f"{customers} customers, {orders} orders, {revenue} revenue"

    except Exception as e:
        log_message += f" GraphQL query failed: {e}"

    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(log_message + "\n")
