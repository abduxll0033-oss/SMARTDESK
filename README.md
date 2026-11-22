\# 🎧 SMARTDESK – IT Help Desk \& Troubleshooting System



SMARTDESK is a Python-based IT Help Desk application built with Streamlit. It helps manage technical support tickets, monitor ticket status, perform basic network diagnostics, and access troubleshooting guidance through a simple dashboard.



\## 🚀 Features



\- \*\*Ticket Management:\*\* Create and manage technical support tickets.

\- \*\*Dashboard Overview:\*\* Monitor total, open, in-progress, and resolved tickets.

\- \*\*Support Analytics:\*\* View ticket statistics by status and category.

\- \*\*Search \& Filters:\*\* Search tickets and filter by status, priority, and category.

\- \*\*Network Diagnostics:\*\* Run IP configuration, Ping tests, and DNS lookups.

\- \*\*Troubleshooting Knowledge Base:\*\* Access solutions for common technical issues.

\- \*\*CSV Reports:\*\* Download support ticket reports.

\- \*\*Database Integration:\*\* Store ticket information using SQLite.



\## 🛠️ Technologies Used



\- Python

\- Streamlit

\- SQLite

\- Pandas

\- Git \& GitHub



\## 📁 Project Structure



```text

SMARTDESK/

│

├── app.py

├── requirements.txt

├── .gitignore

├── README.md

└── smartdesk.db (generated locally)

```



\## 💻 Installation \& Setup



\### 1. Clone the repository



```bash

git clone https://github.com/abduxll0033-oss/SMARTDESK.git

```



\### 2. Open the project folder



```bash

cd SMARTDESK

```



\### 3. Create a virtual environment



```bash

python -m venv .venv

```



\### 4. Activate the virtual environment



For Windows PowerShell:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



\### 5. Install dependencies



```bash

pip install -r requirements.txt

```



\### 6. Run the application



```bash

streamlit run app.py

```



\### 7. Open in your browser



```text

http://localhost:8501

```



\## 🌐 Network Diagnostics



SMARTDESK includes three basic network diagnostic tools:



1\. IP Configuration – Displays network adapter and IP information.

2\. Ping Test – Checks connectivity to 8.8.8.8.

3\. DNS Lookup – Checks domain name resolution for google.com.



These diagnostic commands are designed for Windows environments.



\## 📊 Database



SMARTDESK uses SQLite to store support ticket information, including:



\- Ticket ID

\- Customer Name

\- Technical Issue

\- Issue Category

\- Priority

\- Ticket Status



The database is created locally when the application runs.



\## 🎯 Project Objective



The objective of SMARTDESK is to provide a simple and practical IT support management system that combines ticket tracking, basic network troubleshooting, analytics, and support documentation in one application.



\## 👨‍💻 Developer



\*\*Abdul Wahab L\*\*



GitHub: https://github.com/abduxll0033-oss



\## 📄 License



This project is available for educational and personal learning purposes.



