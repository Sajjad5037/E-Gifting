```python
# app.py

import streamlit as st
from datetime import datetime
import uuid

# -----------------------------
# APP CONFIG
# -----------------------------

st.set_page_config(
    page_title="Client Portal Workflow Demo",
    layout="wide"
)

# -----------------------------
# SESSION STATE
# -----------------------------

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "connected_services" not in st.session_state:
    st.session_state.connected_services = []

if "workflow_logs" not in st.session_state:
    st.session_state.workflow_logs = []

if "webhook_events" not in st.session_state:
    st.session_state.webhook_events = []

if "clients" not in st.session_state:
    st.session_state.clients = []

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def create_log_entry(action_name, status_name):

    st.session_state.workflow_logs.append({
        "id": str(uuid.uuid4())[:8],
        "action": action_name,
        "status": status_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


def simulate_webhook_event(event_name, payload_data):

    st.session_state.webhook_events.append({
        "event": event_name,
        "payload": payload_data,
        "received_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("Client Portal")

selected_page = st.sidebar.radio(
    "Navigation",
    [
        "Login",
        "Connect Services",
        "Workflow Triggers",
        "Webhook Events",
        "Admin Dashboard"
    ]
)

# -----------------------------
# LOGIN PAGE
# -----------------------------

if selected_page == "Login":

    st.title("Client Login Portal")

    user_email = st.text_input("Email")

    user_password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if user_email and user_password:

            st.session_state.logged_in_user = user_email

            if user_email not in st.session_state.clients:

                st.session_state.clients.append(
                    user_email
                )

            create_log_entry(
                action_name="User Login",
                status_name="Success"
            )

            st.success(
                f"Logged in as {user_email}"
            )

        else:
            st.error("Please provide credentials.")

    if st.session_state.logged_in_user:

        st.info(
            f"Current User: "
            f"{st.session_state.logged_in_user}"
        )

# -----------------------------
# CONNECT SERVICES PAGE
# -----------------------------

elif selected_page == "Connect Services":

    st.title("External Service Connections")

    if not st.session_state.logged_in_user:

        st.warning("Please log in first.")
        st.stop()

    available_services = [
        "Tremendous Connect",
        "Stripe",
        "Slack",
        "HubSpot"
    ]

    selected_service_name = st.selectbox(
        "Select Service",
        available_services
    )

    if st.button("Connect Service"):

        if (
            selected_service_name
            not in st.session_state.connected_services
        ):

            st.session_state.connected_services.append(
                selected_service_name
            )

            create_log_entry(
                action_name=(
                    f"Connected "
                    f"{selected_service_name}"
                ),
                status_name="Connected"
            )

            simulate_webhook_event(
                event_name="service.connected",
                payload_data={
                    "service": selected_service_name,
                    "user": (
                        st.session_state.logged_in_user
                    )
                }
            )

            st.success(
                f"{selected_service_name} "
                f"connected successfully."
            )

        else:
            st.info("Service already connected.")

    st.subheader("Connected Services")

    for service_name in (
        st.session_state.connected_services
    ):

        st.write(f"- {service_name}")

# -----------------------------
# WORKFLOW TRIGGERS PAGE
# -----------------------------

elif selected_page == "Workflow Triggers":

    st.title("Workflow Trigger Center")

    if not st.session_state.logged_in_user:

        st.warning("Please log in first.")
        st.stop()

    workflow_action_name = st.selectbox(
        "Select Workflow",
        [
            "Send Reward",
            "Start Client Onboarding",
            "Generate Report",
            "Sync Client Data"
        ]
    )

    if st.button("Run Workflow"):

        create_log_entry(
            action_name=workflow_action_name,
            status_name="Triggered"
        )

        simulate_webhook_event(
            event_name="workflow.triggered",
            payload_data={
                "workflow": workflow_action_name,
                "user": (
                    st.session_state.logged_in_user
                )
            }
        )

        st.success(
            f"{workflow_action_name} "
            f"workflow triggered."
        )

# -----------------------------
# WEBHOOK EVENTS PAGE
# -----------------------------

elif selected_page == "Webhook Events":

    st.title("Webhook Event Viewer")

    if len(
        st.session_state.webhook_events
    ) == 0:

        st.info(
            "No webhook events received yet."
        )

    else:

        for event_data in reversed(
            st.session_state.webhook_events
        ):

            with st.expander(
                f"{event_data['event']} | "
                f"{event_data['received_at']}"
            ):

                st.json(event_data)

# -----------------------------
# ADMIN DASHBOARD PAGE
# -----------------------------

elif selected_page == "Admin Dashboard":

    st.title("Admin Dashboard")

    total_clients_count = len(
        st.session_state.clients
    )

    total_services_count = len(
        st.session_state.connected_services
    )

    total_logs_count = len(
        st.session_state.workflow_logs
    )

    (
        metric_column_1,
        metric_column_2,
        metric_column_3
    ) = st.columns(3)

    metric_column_1.metric(
        "Clients",
        total_clients_count
    )

    metric_column_2.metric(
        "Connected Services",
        total_services_count
    )

    metric_column_3.metric(
        "Workflow Logs",
        total_logs_count
    )

    st.subheader("Workflow Activity Logs")

    if len(
        st.session_state.workflow_logs
    ) == 0:

        st.info(
            "No workflow activity yet."
        )

    else:

        for log_data in reversed(
            st.session_state.workflow_logs
        ):

            st.write(
                f"[{log_data['timestamp']}] "
                f"{log_data['action']} "
                f"({log_data['status']})"
            )
```
