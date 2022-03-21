from pydantic import BaseModel, Field
from typing import List

class login(BaseModel):
    email : str = Field(... , example = "nntan2808@gmail.com" , regex="(\W|^)[\w.+\-]*@gmail\.com(\W|$)")
    password : str = Field(... , example = "12345678" , min_length = 8 )

class user(BaseModel):
    name : str = Field(... , example = "Tan")
    email : str = Field(... , example = "nntan2808@gmail.com" , regex="(\W|^)[\w.+\-]*@gmail\.com(\W|$)")
    password : str = Field(... , example = "12345678" , min_length = 8 )

class showUser(BaseModel):
    name : str = Field(... , example = "Tan")
    email : str = Field(... , example = "nntan2808@gmail.com")
    class Config:
         orm_mode = True

class food(BaseModel):
    store_id : int = Field(... , example = "1")
    category: str = Field(... , example = "cơm")
    subCategory: str = Field(... , example = "cơm tấm")
    price : int = Field(... , example = "30000")

class showFood(BaseModel):
    id : int = Field(... , example = "1")
    category: str = Field(... , example = "cơm")
    subCategory: str = Field(... , example = "cơm tấm")
    price : int = Field(... , example = "30000")
    class Config:
        orm_mode = True

class store(BaseModel):
    address: str = Field(... , example = "123 Lê Đại Hành")
    name: str = Field(... , example = "Cơm bình dân")

class showStore(BaseModel):
    id : int = Field(... , example = "1" , alias = "id")
    address: str = Field(... , example = "123 Lê Đại Hành")
    name: str = Field(... , example = "Cơm bình dân")
    food: List[showFood]
    class Config:
        orm_mode = True

class foodOrder(BaseModel):
    id: int = Field(..., example="1")
    quanlity : int = Field(... , example = "1")

class order(BaseModel):
    store_id: int = Field(..., example="1")
    foods : List[foodOrder]

class showOrder(BaseModel):
    id: int = Field(..., example="1")
    user_id : int = Field(..., example="1")
    address: str = Field(... , example = "123 Lê Đại Hành")
    store_name: str = Field(... , example = "Cơm bình dân")
    category: str = Field(... , example = "cơm")
    subCategory: str = Field(... , example = "cơm tấm")
    price : int = Field(... , example = "30000")
    quanlity: int = Field(None, example="1")
    total: int = Field(None, example="30000")
    class Config:
        orm_mode = True

class customReturnFood(BaseModel):
    category: str = Field(None , example = "cơm")
    subCategory: str = Field(None, example="cơm tấm")
    price : int = Field(None , example = "30000")
    quanlity : int = Field(None , example = "1")
    total : int = Field(None , example = "30000")
    class Config:
        orm_mode = True

class customReturnOrder(BaseModel):
    username : str = Field(None , example = "Tan")
    email : str = Field(None  , example = "nntan2808@gmail.com" , regex="(\W|^)[\w.+\-]*@gmail\.com(\W|$)")
    store_name: str = Field(None, example="Cơm bình dân")
    store_address: str = Field(None  , example = "123 Lê Đại Hành")
    foods : List[customReturnFood] = Field([])
    total: int = Field(None, example="100000")
    class Config:
         orm_mode = True




