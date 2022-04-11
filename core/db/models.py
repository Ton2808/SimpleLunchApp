from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BOOLEAN
from sqlalchemy.orm import relationship

from core.db.database import Base


# store one to many with food
# user one to many with order
# Note: Because I think the order is unchangeable, so I didn't create relationship between order with store and food.
# For example if we change the store address the order address history will be change too.

class store(Base):
    __tablename__ = "store"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    address = Column(String, unique=True, nullable=False)
    food = relationship("food", back_populates="store")


class food(Base):
    __tablename__ = "food"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    store_id = Column(Integer, ForeignKey('store.id'), nullable=False)
    category = Column(String, nullable=False)
    subCategory = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    sold_out: Column(BOOLEAN, nullable=False)
    store = relationship("store", back_populates="food")


class user(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    orders = relationship("orders", back_populates="user")


class orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    store_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    category = Column(String, nullable=False)
    subCategory = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quanlity = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    user = relationship("user", back_populates="orders")

# OLTP vs OLAP
# Distributed db


# b-tree vs lstm
# optimize for read
# optimize for write
