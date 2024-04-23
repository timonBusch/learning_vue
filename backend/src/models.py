from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from database import Base

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    full_name = Column(String)
    phone = Column(String)
    company = Column(String)
    
    customer = relationship("Order", back_populates="order_owner")

   
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    delivery_date = Column(Date, default=None, nullable=True)
    capture_date = Column(Date)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    
    order_owner = relationship("Customer", back_populates="customer")
    items = relationship("OrderItem", back_populates="order_items") 
    

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    width = Column(Integer)
    length = Column(Integer)
    
    product = relationship("OrderItem", back_populates="product")
    
class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    quantity = Column(Integer)
    
    product = relationship("Product", back_populates="product")
    order_items = relationship("Order", back_populates="items")
    
