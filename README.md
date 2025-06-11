# 📦 Terrific Totes Data Pipeline

Welcome to the Terrific Totes data engineering project by Northcoders Team 14 – Duck!  
This project builds a cloud-based data platform to help a fictional company, Terrific Totes, manage and analyse their sales and operations data.


---

## 🚀 Project Overview

This project implements a scalable, event-driven data pipeline using AWS and Python to:

- Extract data from a PostgreSQL database (`totesys`)
- Ingest and store raw data in an Amazon S3 ingestion bucket
- Transform the data into a star-schema format
- Load the transformed data into a data warehouse
- Visualise insights using tools such as Streamlit 

---

## 🌟 Why It Matters

Terrific Totes needed clearer visibility into sales and operational performance.
This pipeline provides:

- Real-time, structured data for decision-making
- Automated workflows for ingestion, transformation, and loading
- Cloud-native scalability and resilience
- Integration with BI tools to support cross-departmental insights 

---

## 💻 Technologies Used

- Python 3.10+
- SQL
- PostgreSQL
- Pandas
- pg8000
- Pytest

## 🌩️ AWS Services

- Amazon S3 – for storing raw and processed data
- AWS Lambda – for event-driven ingestion and transformation
- AWS CloudWatch – for logging and monitoring
- AWS IAM – for secure resource permissions
- AWS Step Functions – to orchestrate multi-step workflows
- Amazon EventBridge – for scheduling and event triggering

## ⚙️ DevOps & Infra

- Terraform – for infrastructure as code
- Streamlit – for building interactive data visualisations

---

## 🛠️ Getting Started

1. Clone the Repository

```bash
git clone https://github.com/Team-Duck-14/project-terrific-totes
cd project-terrific-totes
```

2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Environment Setup

Create a .env file in the root directory with the following (replace with your actual values):

```bash
PGHOST=<your-db-host>
PGDATABASE=<your-database-name>
PGUSER=<your-db-username>
PGPASSWORD=<your-db-password>
AWS_ACCESS_KEY_ID=<your-aws-key>
AWS_SECRET_ACCESS_KEY=<your-aws-secret>
```

You may also need .env.test and .env.development files if working across environments.

## 🧪 Running Tests

After setting up the environment, you can run tests with:

```bash
pytest
```
To see test coverage:
```bash
pytest --cov
```
Ensure the database and any required AWS resources are running before executing tests.

## 📊 Visualisation

We use Streamlit for data visualisation. To run the dashboard locally:
```bash
streamlit run app.py
```

## 👥 Contributions

This was a collaborative team project as part of the Northcoders Data Engineering Bootcamp.