from core.Schemas import Schemas
from fastapi import Depends, Body, Query, APIRouter
from core.db.database import get_db
from sqlalchemy.orm import Session
from typing import List
from app.repositories import user_re

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/', description="Create a user", response_model=Schemas.showUser)
def createUser(user: Schemas.user = Body(..., embed=True), db: Session = Depends(get_db)):
    return user_re.createUser(user, db)


@router.post('/{user_id}/order/',
             description="Create orders for a user , you can create multi food in the same store at the same time by putting a \, then create a new dict in the foods[]")
def createOrders(login: Schemas.login, order: Schemas.order, db: Session = Depends(get_db)):
    # Check all the condition is valid
    return user_re.createOrders(login, order, db)


@router.get('/', description="Get all user info", response_model=List[Schemas.showUser])
def getAllUser(db: Session = Depends(get_db)):
    return user_re.getAllUser(db)


@router.get('/{user_id}/password/', description="Get user password by email")
def getUserPassword(email: str, db: Session = Depends(get_db)):
    return user_re.getUserPassword(email, db)


@router.get('/{user_id}/order/', description="Get all order", response_model=List[Schemas.showOrder])
def getOrders(email: str = Query(..., example="nntan2808@gmail.com"), password: str = Query(...),
              db: Session = Depends(get_db)):
    return user_re.getOrders(email, password, db)


@router.put('/{user_id}/password/')
def changePassword(email: str = Query(None, description="Please enter your email", example="nntan2808@gmail.com"),
                   oldPassword: str = Query(None, description="Please enter your old passowrd", example="12345678"),
                   newPassowrd: str = Query(None, description="Please enter your new password", example="123456789"),
                   db: Session = Depends(get_db)):
    return user_re.changePassword(email, oldPassword, newPassowrd, db)


@router.delete('/{user_id}/')
def deleteUser(email: str = Query(..., example="nntan2808@gmail.com"),
               password: str = Query(..., example="12345678", min_length=8),
               db: Session = Depends(get_db)):
    return user_re.deleteUser(email, password, db)

# Todo Create a delete operation to cancel an order
