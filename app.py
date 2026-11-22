
import streamlit as st
import sqlite3
import pandas as pd
import subprocess
# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="SMARTDESK | IT Support",
    page_icon="🎧",
    layout="wide"
)

# --------------------------------
# DATABASE CONNECTION
# --------------------------------

def get_connection():
    return sqlite3.connect("smartdesk.db")

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer TEXT,
    issue TEXT,
    category TEXT,
    priority TEXT,
    status TEXT
)
""")

conn.commit()

# --------------------------------
# TROUBLESHOOTING KNOWLEDGE BASE
# --------------------------------

solutions = {
    "Network": [
        "Check Wi-Fi or Ethernet connection.",
        "Restart the router.",
        "Check IP configuration using ipconfig.",
        "Test DNS resolution."
    ],

    "Login": [
        "Verify username and password.",
        "Check internet connectivity.",
        "Check whether the account is locked.",
        "Use the password reset process if needed."
    ],

    "Software": [
        "Restart the application.",
        "Check for available updates.",
        "Review the error message.",
        "Reinstall only if appropriate."
    ],

    "Hardware": [
        "Check power supply.",
        "Inspect cable connections.",
        "Restart the device.",
        "Check device status."
    ]
}

# --------------------------------
# CUSTOM HEADER
# --------------------------------

st.title("🎧 SMARTDESK")
st.caption("Professional IT Help Desk & Troubleshooting System")

st.divider()

# --------------------------------
# FETCH DATABASE RECORDS
# --------------------------------

def load_tickets():
    return pd.read_sql_query(
        "SELECT * FROM tickets ORDER BY id DESC",
        conn
    )

df = load_tickets()

# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.title("SMARTDESK")
st.sidebar.caption("Support Management")

search = st.sidebar.text_input(
    "🔍 Search Customer or Ticket"
)

status_filter = st.sidebar.selectbox(
    "Filter by Status",
    ["All", "Open", "In Progress", "Resolved"]
)

priority_filter = st.sidebar.selectbox(
    "Filter by Priority",
    ["All", "High", "Medium", "Low"]
)

category_filter = st.sidebar.selectbox(
    "Filter by Category",
    ["All", "Network", "Login", "Software", "Hardware"]
)

# --------------------------------
# DASHBOARD STATISTICS
# --------------------------------

st.header("Dashboard Overview")

total = len(df)

open_count = len(df[df["status"] == "Open"])

progress_count = len(
    df[df["status"] == "In Progress"]
)

resolved_count = len(
    df[df["status"] == "Resolved"]
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Tickets", total)
c2.metric("Open Tickets", open_count)
c3.metric("In Progress", progress_count)
c4.metric("Resolved", resolved_count)

st.divider()

# --------------------------------
# ANALYTICS
# --------------------------------

st.header("📊 Support Analytics")

left, right = st.columns(2)

with left:
    st.subheader("Tickets by Status")

    if not df.empty:
        status_data = (
            df["status"]
            .value_counts()
            .reindex(
                ["Open", "In Progress", "Resolved"],
                fill_value=0
            )
        )

        st.bar_chart(status_data)

    else:
        st.info("No ticket data available.")

with right:
    st.subheader("Tickets by Category")

    if not df.empty:
        category_data = df["category"].value_counts()
        st.bar_chart(category_data)

    else:
        st.info("No ticket data available.")

st.divider()

# --------------------------------
# CREATE NEW TICKET
# --------------------------------

st.header("➕ Create Support Ticket")

with st.form("create_ticket"):

    customer = st.text_input("Customer Name")

    issue = st.text_area(
        "Describe the Technical Problem"
    )

    category = st.selectbox(
        "Issue Category",
        ["Network", "Login", "Software", "Hardware"]
    )

    priority = st.selectbox(
        "Priority",
        ["Low", "Medium", "High"]
    )

    submit = st.form_submit_button(
        "Create Ticket"
    )

    if submit:

        if customer.strip() and issue.strip():

            cursor.execute("""
                INSERT INTO tickets
                (customer, issue, category, priority, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                customer.strip(),
                issue.strip(),
                category,
                priority,
                "Open"
            ))

            conn.commit()

            st.success("Ticket created successfully!")

            st.rerun()

        else:
            st.error("Please enter customer name and problem.")

st.divider()

# --------------------------------
# SEARCH AND FILTER
# --------------------------------

st.header("🎫 Support Ticket Management")

filtered = df.copy()

if search:
    filtered = filtered[
        filtered["customer"].str.contains(
            search, case=False, na=False
        )
        |
        filtered["id"].astype(str).str.contains(
            search, case=False
        )
    ]

if status_filter != "All":
    filtered = filtered[
        filtered["status"] == status_filter
    ]

if priority_filter != "All":
    filtered = filtered[
        filtered["priority"] == priority_filter
    ]

if category_filter != "All":
    filtered = filtered[
        filtered["category"] == category_filter
    ]

st.caption(f"Showing {len(filtered)} matching tickets")

# --------------------------------
# DISPLAY TICKETS
# --------------------------------

if not filtered.empty:

    for _, ticket in filtered.iterrows():

        with st.expander(
            f"Ticket #{ticket['id']} | "
            f"{ticket['customer']} | "
            f"{ticket['status']}"
        ):

            st.write("**Customer:**", ticket["customer"])

            st.write("**Problem:**", ticket["issue"])

            st.write("**Category:**", ticket["category"])

            st.write("**Priority:**", ticket["priority"])

            st.write("**Current Status:**", ticket["status"])

            st.subheader("🔧 Troubleshooting Suggestions")

            for step in solutions.get(
                ticket["category"], []
            ):
                st.write("•", step)

            ticket_id = int(ticket["id"])

            new_status = st.selectbox(
                "Update Ticket Status",

                ["Open", "In Progress", "Resolved"],

                index=[
                    "Open",
                    "In Progress",
                    "Resolved"
                ].index(ticket["status"]),

                key=f"status_{ticket_id}"
            )

            if st.button(
                "Save Changes",
                key=f"save_{ticket_id}"
            ):

                cursor.execute(
                    "UPDATE tickets SET status=? WHERE id=?",
                    (new_status, ticket_id)
                )

                conn.commit()

                st.success("Ticket updated successfully!")

                st.rerun()

else:

    st.info("No matching support tickets found.")

st.divider()

# --------------------------------
# NETWORK DIAGNOSTICS MODULE
# --------------------------------

st.divider()

st.header("🌐 Network Diagnostics")

st.write(
    "Run basic network troubleshooting tests "
    "directly from SMARTDESK."
)

def run_diagnostic(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15,
            shell=False,
            errors="replace"
        )

        output = result.stdout + result.stderr

        if output.strip():
            return output

        return f"Command finished with exit code {result.returncode}"

    except subprocess.TimeoutExpired:
        return "Diagnostic timed out. Please try again."

    except FileNotFoundError:
        return "Windows could not find the required command."

    except Exception as error:
        return f"Diagnostic error: {error}"


tab1, tab2, tab3 = st.tabs([
    "IP Configuration",
    "Ping Test",
    "DNS Lookup"
])

# IP CONFIGURATION

with tab1:

    st.subheader("Computer Network Information")

    st.write(
        "Displays your IP address, gateway, "
        "subnet mask and network adapters."
    )

    if st.button("Run IP Configuration"):

        with st.spinner("Checking network configuration..."):

            output = run_diagnostic(["ipconfig", "/all"])

            st.code(output, language="text")


# PING TEST

with tab2:

    st.subheader("Internet Connectivity Test")

    st.write("Target: 8.8.8.8")

    st.write(
        "Checks whether your computer can communicate "
        "with Google's public DNS server."
    )

    if st.button("Start Ping Test"):

        with st.spinner("Testing network connectivity..."):

            output = run_diagnostic([
                "ping",
                "-n",
                "4",
                "8.8.8.8"
            ])

            st.code(output, language="text")

            if "Reply from" in output:
                st.success("Ping replies received.")

            elif "Request timed out" in output:
                st.warning(
                    "No ping reply received. "
                    "The destination may block ICMP traffic."
                )

            else:
                st.warning(
                    "Check the diagnostic output for the result."
                )


# DNS LOOKUP

with tab3:

    st.subheader("Domain Name Resolution")

    st.write("Target domain: google.com")

    st.write(
        "Checks whether DNS can resolve a domain name "
        "into an IP address."
    )

    if st.button("Run DNS Lookup"):

        with st.spinner("Checking DNS resolution..."):

            output = run_diagnostic([
                "nslookup",
                "google.com"
            ])

            st.code(output, language="text")

            if "Address:" in output:
                st.success("DNS returned an address.")
            else:
                st.warning(
                    "Check the DNS output for possible resolution issues."
                )

# --------------------------------
# REPORT DOWNLOAD
# --------------------------------

st.header("📥 Download Support Report")

if not df.empty:

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Ticket Report (CSV)",
        data=csv_data,
        file_name="smartdesk_support_report.csv",
        mime="text/csv"
    )

else:

    st.info("Create tickets to generate a report.")

# ----------------------------------
# SMARTDESK KNOWLEDGE BASE
# ----------------------------------

st.divider()

st.header("📚 Technical Support Knowledge Base")

st.write(
    "Find common technical problems and follow "
    "step-by-step troubleshooting solutions."
)

knowledge_base = {
    "Internet Connection Problem": [
        "Check whether Wi-Fi is enabled.",
        "Restart your router.",
        "Run ipconfig in Command Prompt.",
        "Ping 8.8.8.8 to test connectivity.",
        "Contact your network administrator if the issue continues."
    ],

    "DNS Resolution Error": [
        "Open Command Prompt.",
        "Run ipconfig /flushdns.",
        "Run nslookup google.com.",
        "Check your DNS server settings.",
        "Restart your network connection."
    ],

    "Software Installation Error": [
        "Check available disk space.",
        "Verify the installer is downloaded completely.",
        "Check Windows compatibility.",
        "Run the installer with appropriate permissions.",
        "Review the installation error message."
    ],

    "Windows Slow Performance": [
        "Open Task Manager.",
        "Check CPU and memory usage.",
        "Disable unnecessary startup applications.",
        "Remove temporary files.",
        "Restart your computer."
    ],

    "Login Problem": [
        "Verify your username.",
        "Check your password and keyboard layout.",
        "Check your internet connection.",
        "Use the official password reset option.",
        "Contact the administrator if access is still denied."
    ]
}

search_problem = st.text_input(
    "🔍 Search Technical Problem"
)

filtered_problems = [
    problem for problem in knowledge_base
    if search_problem.lower() in problem.lower()
]

if not search_problem:
    filtered_problems = list(knowledge_base.keys())

if filtered_problems:

    selected_problem = st.selectbox(
        "Select a Problem",
        filtered_problems
    )

    st.subheader("🛠️ Troubleshooting Steps")

    for index, solution in enumerate(
        knowledge_base[selected_problem], 1
    ):
        st.write(f"**Step {index}:** {solution}")

    st.success("Follow these steps to troubleshoot the issue.")

else:
    st.warning("No matching problem found. Try another keyword.")

# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "SMARTDESK | IT Help Desk & Troubleshooting System"
)

conn.close()
