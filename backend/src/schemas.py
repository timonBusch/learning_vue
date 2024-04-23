from pydantic import BaseModel
from datetime import date
from typing import Optional

class CustomerBase(BaseModel):
    email: str
    full_name: str
    phone: int
    company: str
    
# Give the customer class additional parameters only for creating it e.g. passwords
class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    
    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    product_id: int
    order_id: int
    quantity: int
    
class OrderItemCreate(OrderItemBase):
    pass
    
class OrderItem(OrderItemBase):
    id: int
    
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    capture_date: date
    
class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int 
    customer_id: int
    delivery_date: Optional[date] = None
    items: list[OrderItem] = []
    
    class Config:
        from_attributes = True
 
class ProductBase(BaseModel):
    name: str
    width: int
    length: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    
    class Config:
        from_attributes = True
        

