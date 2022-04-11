from core.Schemas import Schemas
from core.db import models
from fastapi import Depends, Body, HTTPException, Query, status, APIRouter
from core.db.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.repositories import store_re

router = APIRouter(prefix='/store', tags=['store'])


@router.post('/', description="Create a new store", response_model=Schemas.showStore)
def createStore(store: Schemas.store = Body(..., embed=True), db: Session = Depends(get_db)):
    return store_re.createStore(store, db)


@router.post('/{store_id}/food/', description="Create a new food for a store", response_model=Schemas.showFood)
def createFood(food: Schemas.food = Body(..., embed=True), db: Session = Depends(get_db)):
    return store_re.createFood(food, db)


@router.get('/', description="Get all the store", response_model=List[Schemas.showStore])
def getAllStore(db: Session = Depends(get_db)):
    return store_re.getAllStore(db)


@router.get('/{store_id}/food/', description="Get all the food of a store", response_model=Schemas.showStore)
def getFoodsInAStore(store_id: int = Query(..., description="Please enter the store id"),
                     db: Session = Depends(get_db)):
    return store_re.getFoodInAStore(store_id, db)


@router.put('/{store_id}/', description="Fix store information", response_model=Schemas.showStore)
def updateStore(storeUpdateId: int = Query(..., example="1"), updateInfo: Schemas.store = Body(..., embed=True),
                db: Session = Depends(get_db)):
    return store_re.updateStore(storeUpdateId, updateInfo, db)


@router.delete('/{store_id}/', description="Delete a store")
def deleteStore(storeDeleteId: int = Query(..., example="1"), db: Session = Depends(get_db)):
    return store_re.deleteStore(storeDeleteId, db)


# Delete a food
@router.delete('/{food_id}/', description="Delete a food in a store")
def deleteFood(foodDeleteId: int = Query(..., example=1), db: Session = Depends(get_db)):
    return store_re.deleteFood(foodDeleteId, db)

# Todo add update for food
