import Schemas, models
from fastapi import Depends, Body , HTTPException, Query, status, APIRouter
from database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix = '/user' , tags = ['user'])

#This will create a user, the email must be unique and end with @gmail.com and the length of the password >= 8. Else it will return error.
@router.post('/'  , description= "Create a user" , response_model = Schemas.showUser)
def createUser(user : Schemas.user = Body(... , embed = True), db : Session = Depends(get_db)):
    users = db.query(models.user).all()
    for i in users:
        if user.email == i.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exited")
    newUser = models.user(name = user.name, email = user.email , password = user.password)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser


@router.post('/{user_id}/order/' , description = "Create orders for a user , you can create multi food in the same store at the same time by putting a \, then create a new dict in the foods[]")
def createOrders(login : Schemas.login , order : Schemas.order , db : Session = Depends(get_db)):
    # Check all the condition is valid
    user = db.query(models.user).filter(models.user.email == login.email).first()
    if not user or (user and user.password != login.password):
        raise HTTPException(status_code=400, detail="Wrong email or password")
    store = db.query(models.store).filter(models.store.id == order.store_id).first()
    if not store:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No such store with id {order.store_id} found")
    food_id = []
    for i in store.food:
        food_id.append(i.id)
    for food in order.foods:
        if food.id not in food_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,  detail=f"No such food id {food.id} found in the store with id {order.store_id}")

    # Return a custom order output and update the order database
    ans = Schemas.customReturnOrder()
    ans.store_address = store.address
    ans.store_name = store.name
    ans.username = user.name
    ans.email = user.email
    ans.total = 0
    for food in order.foods:
        orderfood = db.query(models.food).filter(models.food.id == food.id).first()
        new_order = models.orders(user_id = user.id , store_name = store.name , address = store.address , category = orderfood.category , subCategory = orderfood.subCategory , price = orderfood.price , quanlity = food.quanlity , total = food.quanlity * orderfood.price)

        ans.total += food.quanlity * orderfood.price
        temp = Schemas.customReturnFood()
        temp.category = new_order.category
        temp.subCategory = new_order.subCategory
        temp.price = new_order.price
        temp.quanlity = new_order.quanlity
        temp.total = new_order.total
        ans.foods.append(temp)

        db.add(new_order)
        db.commit()
        db.refresh(new_order)
    return ans

# This will return all the username and email
@router.get('/' , description= "Get all user info" , response_model = List[Schemas.showUser])
def getUser(db : Session = Depends(get_db)):
    return db.query(models.user).all()

# This will return the user password if you give it your email
@router.get('/{user_id}/password/' , description= "Get user password by email" )
def getUserPassword(email : str , db : Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.email == email)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not existed")
    return {"Your pass word is: " : user.first().password}

#This will get all the order of a user
@router.get('/{user_id}/order/' , description = "Get all order" , response_model = List[Schemas.showOrder])
def getOrders(email : str = Query(... , example = "nntan2808@gmail.com")  , password : str = Query(... , example = "12345678" , min_length = 8 ), db : Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.email == email).first()
    if not user or (user and user.password != password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong email or password")
    order = db.query(models.orders).filter(models.orders.user_id == user.id).all()
    return order

# Change the password of a user
@router.put('/{user_id}/password/')
def changePassword(email : str = Query(None , description="Please enter your email" , example = "nntan2808@gmail.com") ,
                   oldPassword : str = Query(None , description="Please enter your old passowrd" , example = "12345678"),
                   newPassowrd: str = Query(None, description="Please enter your new password" , example = "123456789"),
                   db : Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.email == email).first()
    if user.password == oldPassword:
        db.query(models.user).filter(models.user.email == email).update({models.user.password: newPassowrd}, synchronize_session=False)
        db.commit()
        return "Your password had been updated"
    else:
        raise HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE , detail = "Wrong password")

# Delete a user account
@router.delete('/{user_id}/')
def deleteUser(email : str = Query(... , example = "nntan2808@gmail.com")  , password : str = Query(... , example = "12345678" , min_length = 8 ), db : Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.email == email).first()
    if not user or (user and user.password != password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong email or password")
    db.query(models.orders).filter(models.orders.user_id == user.id).delete()
    db.query(models.user).filter(models.user.email == email).delete()
    db.commit()
    return {f"user with email {email} has been deleted"}

# Todo Create a delete operation to cancel an order