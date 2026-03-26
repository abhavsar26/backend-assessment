from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models.customer import Customer
from services.ingestion import fetch_all_customers, upsert_customer

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/ingest")
def ingest(db: Session = Depends(get_db)):
    customers = fetch_all_customers()

    count = 0
    for c in customers:
        upsert_customer(db, c)
        count += 1

    db.commit()

    return {"status": "success", "records_processed": count}


@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * limit

    customers = db.query(Customer).offset(offset).limit(limit).all()
    total = db.query(Customer).count()

    return {
        "data": customers,
        "total": total,
        "page": page,
        "limit": limit
    }


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(
        Customer.customer_id == customer_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Not found")

    return customer