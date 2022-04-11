from core.db import models
from core.db.database import get_db
from core.Schemas import Schemas
from fastapi import Depends, Body, HTTPException, status
from sqlalchemy.orm import Session


def getAllUser(db: Session = Depends(get_db)):
    return db.query(models.user).all()


def getUserByEmail(email: str, db: Session = Depends(get_db)):
    return db.query(models.user).filter(models.user.email == email).first()


def createUser(user: Schemas.user = Body(..., embed=True), db: Session = Depends(get_db)):
    users = getAllUser(db)
    for i in users:
        if user.email == i.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exited")
    newUser = models.user(name=user.name, email=user.email, password=user.password)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser


def getUserPassword(email: str, db: Session = Depends(get_db)):
    user = getUserByEmail(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not existed")
    return user.password


def changePassword(email: str, oldPassword: str, newPassword: str, db: Session = Depends(get_db)):
    user = getUserByEmail(email, db)
    if user.password == oldPassword:
        db.query(models.user).filter(models.user.email == email).update({models.user.password: newPassword},
                                                                        synchronize_session=False)
        db.commit()
        return "Your password had been updated"
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Wrong password")


def getOrders(email: str, password: str, db: Session = Depends(get_db)):
    user = getUserByEmail(email, db)
    if not user or (user and user.password != password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong email or password")
    order = db.query(models.orders).filter(models.orders.user_id == user.id).all()
    return order


def deleteUser(email: str, password: str, db):
    user = getUserByEmail(email, db)
    if not user or (user and user.password != password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong email or password")
    db.query(models.orders).filter(models.orders.user_id == user.id).delete()
    db.query(models.user).filter(models.user.email == email).delete()
    db.commit()
    return {f"user with email {email} has been deleted"}


def createOrders(login: Schemas.login, order: Schemas.order, db: Session = Depends(get_db)):
    user = getUserByEmail(login.email)
    if not user or (user and user.password != login.password):
        raise HTTPException(status_code=400, detail="Wrong email or password")
    store = db.query(models.store).filter(models.store.id == order.store_id).first()
    if not store:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No such store with id {order.store_id} found")
    food_id = []
    for i in store.food:
        food_id.append(i.id)
    for food in order.foods:
        if food.id not in food_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"No such food id {food.id} found in the store with id {order.store_id}")

    ans = Schemas.customReturnOrder(store_address=store.address,
                                    store_name=store.name,
                                    username=user.name,
                                    email=user.email,
                                    total=0)
    for food in order.foods:
        orderfood = db.query(models.food).filter(models.food.id == food.id).first()
        new_order = models.orders(user_id=user.id, store_name=store.name, address=store.address,
                                  category=orderfood.category, subCategory=orderfood.subCategory, price=orderfood.price,
                                  quanlity=food.quanlity, total=food.quanlity * orderfood.price)

        ans.total += food.quanlity * orderfood.price
        temp = Schemas.customReturnFood(category=new_order.category,
                                        subCategory=new_order.subCategory,
                                        price=new_order.price,
                                        quanlity=new_order.quanlity,
                                        total=new_order.total)
        ans.foods.append(temp)
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
    return ans
