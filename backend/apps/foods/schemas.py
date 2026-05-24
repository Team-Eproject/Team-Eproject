from pydantic import BaseModel, Field
from typing import List

class Ingredient(BaseModel):
    name: str = Field(description="食材名")
    quantity: str = Field(description="数量")
    unit: str = Field(description="単位")

class Menu(BaseModel):
    menuId: str = Field(description="メニューID")    
    menuName: str = Field(description="料理名")    
    servingCount: int = Field(description="何人前か")    
    ingredients: List[Ingredient]    
    instructions: List[str]

class Menus(BaseModel):
    menus: List[Menu]


