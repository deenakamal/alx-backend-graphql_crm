from datetime import datetime

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
