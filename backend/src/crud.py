from sqlalchemy.orm import Session
import models
import schemas
from datetime import date


# Customer

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()  

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()  

def get_customer_by_email(db: Session, email: str):
    return db.query(models.Customer).filter(models.Customer.email == email).first()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(
        email=customer.email, full_name=customer.full_name, phone=customer.phone,
        company=customer.company
        )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customer_by_id(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def delete_customer_by_id(db: Session, customer_id: int):
    customer = get_customer_by_id(db=db, customer_id=customer_id)
    delete_orders_by_customer_id(db=db, customer_id=customer_id)
    db.delete(customer)
    db.commit()
    return customer

# Order

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_customer_order(db: Session, order: schemas.OrderCreate, customer_id: int):
    db_order = models.Order(capture_date=order.capture_date, customer_id=customer_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders_by_customer_id(db: Session, customer_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Order).filter(customer_id == models.Order.customer_id).offset(skip).limit(limit).all()

def get_order_items_by_order_id(db: Session, order_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.OrderItem).filter(order_id == models.OrderItem.order_id).offset(skip).limit(limit).all()

def get_order_by_order_id(db: Session, order_id: int):
    return db.query(models.Order).filter(order_id == models.Order.id).first()

def delete_orders_by_customer_id(db: Session, customer_id: int):
    orders = get_orders_by_customer_id(db=db, customer_id=customer_id)
    for order in orders:
        delete_all_items_from_order(db=db, order_id=order.id)
        db.delete(order)
    db.commit()
    return orders

def update_order_del_date_by_id(db: Session, order_id: int, delivery_date: date):
    order = get_order_by_order_id(db=db, order_id=order_id)
    order.delivery_date = delivery_date
    db.commit()
    db.refresh(order)
    return order
    
    

# OrderItem

def create_order_item(db: Session, item: schemas.OrderItemCreate):
    db_order_item = models.OrderItem(order_id=item.order_id, product_id=item.product_id, quantity=item.quantity)
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    return db_order_item

def get_order_items_by_order_id(db: Session, order_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.OrderItem).filter(order_id == models.OrderItem.order_id).offset(skip).limit(limit).all()
    
def get_order_item_by_id(db: Session, order_item_id: int):
    return db.query(models.OrderItem).filter(order_item_id == models.OrderItem.id).first()

def delete_item_from_order_by_id(db: Session, order_id: int, order_item_id: int):
    order_item = get_order_item_by_id(db=db, order_item_id=order_item_id)
    if is_order_item_in_order(db=db, order_id=order_id, order_item_id=order_item_id):
        db.delete(order_item)
    db.commit() 
    return order_item

def delete_all_items_from_order(db: Session, order_id: int):
    order_items = get_order_items_by_order_id(db=db, order_id=order_id)
    order = get_order_by_order_id(db=db, order_id=order_id)
    for item in order_items:
        db.delete(item)
    db.commit()
    db.refresh(order)
    return order_items

def get_order_item_by_id(db: Session, order_item_id: int):
    return db.query(models.OrderItem).filter(order_item_id == models.OrderItem.id)
    
def is_order_item_in_order(db: Session, order_id: int, order_item_id: int):
    order_items = get_order_items_by_order_id(db=db, order_id=order_id)
    for item in order_items:
        if item == get_order_item_by_id(db=db, order_item_id=order_item_id):
            return item
        else:
            return None
    

# Product

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product_by_product_id(db: Session, product_id: int):
    return db.query(models.Product).filter(product_id == models.Product.id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(name=product.name, width=product.width, length=product.length)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product    

def delete_product_by_id(db: Session, product_id: int):
    db_product = get_product_by_product_id(db=db, product_id=product_id)
    db.delete(db_product)
    db.commit()
    return db_product
