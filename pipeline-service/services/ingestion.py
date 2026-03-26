import requests
from sqlalchemy.orm import Session
from models.customer import Customer

FLASK_URL = "http://mock-server:5000/api/customers"

def fetch_all_customers():
    page = 1
    limit = 10
    all_data = []

    while True:
        res = requests.get(f"{FLASK_URL}?page={page}&limit={limit}")
        data = res.json()

        customers = data["data"]
        if not customers:
            break

        all_data.extend(customers)

        if len(customers) < limit:
            break

        page += 1

    return all_data


def upsert_customer(db: Session, customer_data: dict):
    existing = db.query(Customer).filter(
        Customer.customer_id == customer_data["customer_id"]
    ).first()

    if existing:
        for key, value in customer_data.items():
            setattr(existing, key, value)
    else:
        db.add(Customer(**customer_data))