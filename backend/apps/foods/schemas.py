from pydantic import BaseModel, Field
from typing import List

class Ingredient(BaseModel):
    name: str = Field(description="食材名。例: キャベツ")
    quantity: str = Field(description="数量。例: 100")
    unit: str = Field(description="単位。例: g, 個, 本")

class Menu(BaseModel):
    menuId: str = Field(description="メニューID")    
    menuName: str = Field(description="料理名")    
    servingCount: int = Field(description="何人前か")    
    cookingTimeMinutes: int = Field(description="調理時間(分)")    
    ingredients: List[Ingredient]= Field(description="使用する食材一覧") 
    instructions: List[str]= Field(description="調理手順を並べたリスト") 

class Menus(BaseModel):
    menus: List[Menu]


