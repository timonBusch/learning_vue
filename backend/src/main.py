from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import date

from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost"
]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

tags_metadata = [
    
]

# Customer

@app.get("/customers/", response_model=list[schemas.Customer], tags=["Customer"])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers

@app.post("/customers/", response_model=schemas.Customer, tags=["Customer"])
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud.get_customer_by_email(db, email=customer.email)
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_customer(db=db, customer=customer)

@app.get("/customers/{customer_id}/", response_model=schemas.Customer, tags=["Customer"])
def get_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer_by_id(db, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.delete("/customers/{customer_id}", response_model=schemas.Customer, tags=["Customer"])
def delete_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer_by_id(db, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.delete_customer_by_id(db=db, customer_id=customer_id)

# Order

@app.get("/orders/", response_model=list[schemas.Order], tags=["Order"])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@app.post("/orders/{customer_id}/", response_model=schemas.Order, tags=["Order"])
def create_order_for_customer(customer_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)):
    if not crud.get_customer_by_id(db=db, customer_id=customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.create_customer_order(db=db, order=order, customer_id=customer_id)

@app.get("/orders/{customer_id}/", response_model=list[schemas.Order], tags=["Order"])
def get_orders_by_customer_id(customer_id: int, db: Session = Depends(get_db)):
    return crud.get_orders_by_customer_id(db=db, customer_id=customer_id)

@app.put("/orders/{order_id}/", response_model=schemas.Order, tags=["Order"])
def update_order_delivery_date_by_id(order_id: int, delivery_date: date, db: Session = Depends(get_db)):
    return crud.update_order_del_date_by_id(db=db, order_id=order_id, delivery_date=delivery_date)


# OrderItem

@app.get("/order_items/{order_id}", response_model=list[schemas.OrderItem], tags=["OrderItem"])
def get_order_items_from_order_by_id(order_id: int, db: Session = Depends(get_db)):
    return crud.get_order_items_by_order_id(db=db, order_id=order_id)

@app.post("/order_items/", response_model=schemas.OrderItem, tags=["OrderItem"])
def add_item_to_order_by_id(order_item: schemas.OrderItemCreate, db: Session = Depends(get_db)):
    if not crud.get_order_by_order_id(db=db, order_id=order_item.order_id):
        raise HTTPException(status_code=404, detail="Order not found")
    
    if not crud.get_product_by_product_id(db=db, product_id=order_item.product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    
    return crud.create_order_item(db=db, item=order_item)

@app.delete("/order_items/{order_id}", response_model=list[schemas.OrderItem], tags=["OrderItem"])
def delete_all_items_from_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order_by_order_id(db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return crud.delete_all_items_from_order(db=db, order_id=order_id)

@app.delete("/order_items/{order_id}", response_model=schemas.OrderItem, tags=["OrderItem"])
def delete_order_item_from_order(order_id: int, order_item_id: int, db: Session = Depends(get_db)):
    order = crud.get_order_by_order_id(db=db, order_id=order_id)
    order_item = crud.get_order_item_by_id(db=db, order_item_id=order_item_id)
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not order_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.is_order_item_in_order(order_id=order_id, order_item_id=order_item_id):
        raise HTTPException(status_code=400, detail="Item does not belong to order")
    
    return crud.delete_all_items_from_order(db=db, order_id=order_id)

# Product

@app.get("/products/", response_model=list[schemas.Product], tags=["Product"])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    product = crud.get_products(db, skip=skip, limit=limit)
    return product

@app.get("/products/{product_id}", response_model=schemas.Product, tags=["Product"])
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product_by_product_id(db=db, product_id=product_id)

@app.post("/products/", response_model=schemas.Product, tags=["Product"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@app.delete("/products/{product_id}", response_model=schemas.Product, tags=["Product"])
def delete_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_product_id(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.delete_product_by_id(db=db, product_id=product_id)


