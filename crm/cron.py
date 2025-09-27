from datetime import datetime
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client


def log_crm_heartbeat():
    """
    Logs heartbeat message every 5 minutes
    Format: DD/MM/YYYY-HH:MM:SS CRM is alive
    Appends to /tmp/crm_heartbeat_log.txt
    """
    now = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{now} CRM is alive\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message)

    try:
        import requests
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"}
        )
        if response.status_code == 200:
            data = response.json()
            with open("/tmp/crm_heartbeat_log.txt", "a") as f:
                f.write(f"GraphQL hello response: {data}\n")
    except Exception as e:
        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(f"GraphQL check failed: {e}\n")


def update_low_stock():
    now = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{now} - Updating low stock products\n"

    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        mutation = gql(
            """
            mutation {
                updateLowStockProducts {
                    success
                    updatedProducts {
                        name
                        stock
                    }
                }
            }
            """
        )

        result = client.execute(mutation)
        updates = result["updateLowStockProducts"]["updatedProducts"]

        for product in updates:
            log_message += f"Product: {product['name']} | New Stock: {product['stock']}\n"

    except Exception as e:
        log_message += f"GraphQL mutation failed: {e}\n"

    with open("/tmp/low_stock_updates_log.txt", "a") as f:
        f.write(log_message + "\n")
