from core.Schemas import Schemas
from core.db import models
from fastapi import Depends, Body, HTTPException, Query, status, APIRouter
from core.db.database import get_db
from sqlalchemy.orm import Session
from typing import List


def getStoreByAdd(address: str, db: Session = Depends(get_db)):
    return db.query(models.store).filter(models.store.address == address).first()


def getStoreById(id: int, db: Session = Depends(get_db)):
    return db.query(models.store).filter(models.store.id == id).first()


def getFoodsByStoreId(id: int, db: Session = Depends(get_db)):
    return db.query(models.store).filter(models.store.id == id).all()


def getAllStore(db: Session = Depends(get_db)):
    return db.query(models.store).all()


def createStore(store: Schemas.store = Body(..., embed=True), db: Session = Depends(get_db)):
    stores = getStoreByAdd(store.address, db)
    if stores:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The address is already exist")
    newStore = models.store(name=store.name, address=store.address)
    db.add(newStore)
    db.commit()
    db.refresh(newStore)
    return newStore


def createFood(food: Schemas.food = Body(..., embed=True), db: Session = Depends(get_db)):
    is_exist = getFoodsByStoreId(food.store_id, db)
    if len(is_exist) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No such store with id {food.store_id} found")
    newFood = models.food(store_id=food.store_id, category=food.category, subCategory=food.subCategory,
                          price=food.price)
    db.add(newFood)
    db.commit()
    db.refresh(newFood)
    return newFood


def getFoodInAStore(store_id: int, db: Session = Depends(get_db)):
    store = getStoreById(store_id, db)
    if not store:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No such store with id {store_id} found")
    return store


def updateStore(storeUpdateId: int, updateInfo: Schemas.store, db: Session = Depends(get_db)):
    store = db.query(models.store).filter(models.store.id == storeUpdateId)
    if db.query(models.store).filter(models.store.address == updateInfo.address).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The address is already exist")
    if not store.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No such store with id {storeUpdateId} found")
    store.update({models.store.address: updateInfo.address, models.store.name: updateInfo.name})
    db.commit()
    return store.first()


def deleteStore(storeDeleteId: int = Query(..., example="1"), db: Session = Depends(get_db)):
    store = db.query(models.store).filter(models.store.id == storeDeleteId)
    if not store.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No such store with id {storeDeleteId} found")
    db.query(models.food).filter(models.food.store_id == storeDeleteId).delete()
    store.delete()
    db.commit()
    return f"The store with id {storeDeleteId} has been deleted"


def deleteFood(foodDeleteId: int, db: Session = Depends(get_db)):
    food = db.query(models.food).filter(models.food.id == foodDeleteId)
    if not food.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No such food with id {foodDeleteId} found")
    db.query(models.food).filter(models.food.id == foodDeleteId).delete()
    db.commit()
    return f"The food with id {foodDeleteId} has been deleted"
