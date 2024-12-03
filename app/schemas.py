from pydantic import BaseModel, Field
from typing import Optional

class Address(BaseModel):
    city: str = Field(..., title="City", description="The city of the student")
    country: str = Field(..., title="Country", description="The country of the student")

class StudentCreate(BaseModel):
    name: str = Field(..., title="Name", description="The name of the student")
    age: int = Field(..., title="Age", description="The age of the student, must be an integer")
    address: Address

class Addressupdate(BaseModel):
    city:Optional[str] = None
    country:Optional[str] = None

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int]  = None
    address: Optional[Addressupdate] = None
