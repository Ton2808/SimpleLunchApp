import Schemas, models
from fastapi import Depends, Body , HTTPException, Query, status, APIRouter
from database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix = '/store' , tags = ['store'])

#Create a new store
@router.post('/'  , description="Create a new store" , response_model = Schemas.showStore)
def createStore(store: Schemas.store = Body(... , embed = True) , db : Session = Depends(get_db)):
    stores = db.query(models.store).filter(models.store.address == store.address).first()
    if stores:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The address is already exist")
    newStore = models.store(name = store.name , address = store.address)
    db.add(newStore)
    db.commit()
    db.refresh(newStore)
    return newStore

# Add a new food for a store
@router.post('/{store_id}/food/' , description="Create a new food for a store" , response_model = Schemas.showFood)
def createFood(food: Schemas.food = Body(... , embed = True) , db : Session = Depends(get_db)):
    is_exist = db.query(models.store).filter(models.store.id == food.store_id).all()
    if len(is_exist) == 0:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST , detail = f"No such store with id {food.store_id} found")
    newFood = models.food(store_id = food.store_id , category = food.category , subCategory = food.subCategory , price = food.price)
    db.add(newFood)
    db.commit()
    db.refresh(newFood)
    return newFood

# Get all the store with their foods
@router.get('/' , description = "Get all the store" , response_model = List[Schemas.showStore])
def getStore(db : Session = Depends(get_db)):
    store = db.query(models.store).all()
    return store

# Get a specific store with it foods
@router.get('/{store_id}/food/' , description = "Get all the food of a store" , response_model = Schemas.showStore)
def getFood(store_id : int = Query(... , description = "Please enter the store id") , db : Session = Depends(get_db)):
    store = db.query(models.store).filter(models.store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No such store with id {store_id} found")
    return store

# Update the store information
@router.put('/{store_id}/' , description="Fix store information" , response_model=Schemas.showStore)
def updateStore(storeUpdateId : int = Query(... , example = "1") , updateInfo: Schemas.store = Body(... , embed = True), db : Session = Depends(get_db)):
    store = db.query(models.store).filter(models.store.id == storeUpdateId)
    if db.query(models.store).filter(models.store.address == updateInfo.address).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The address is already exist")
    if not store.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No such store with id {storeUpdateId} found")
    store.update({models.store.address : updateInfo.address, models.store.name : updateInfo.name})
    db.commit()
    return store.first()

# Delete a store
@router.delete('/{store_id}/' , description="Delete a store")
def deleteStore(storeDeleteId : int = Query(... , example = "1") , db : Session = Depends(get_db)):
    store = db.query(models.store).filter(models.store.id == storeDeleteId)
    if not store.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No such store with id {storeDeleteId} found")
    db.query(models.food).filter(models.food.store_id == storeDeleteId).delete()
    store.delete()
    db.commit()
    return f"The store with id {storeDeleteId} has been deleted"

# Delete a food
@router.delete('/{food_id}/' , description="Delete a food in a store")
def deleteFood(foodDeleteId : int = Query(... , example = 1) , db : Session = Depends(get_db)):
    food = db.query(models.food).filter(models.food.id == foodDeleteId)
    if not food.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No such food with id {foodDeleteId} found")
    db.query(models.food).filter(models.food.id == foodDeleteId).delete()
    db.commit()
    return f"The food with id {foodDeleteId} has been deleted"

# Todo add update for food

