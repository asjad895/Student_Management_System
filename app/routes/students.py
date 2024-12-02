from fastapi import APIRouter, HTTPException
from app.schemas import StudentCreate, StudentUpdate
from app.services.students import *

router = APIRouter()

@router.post("/", response_model=dict, status_code=201)
async def create_student_api(student: StudentCreate):
    student_id = await create_student(student.model_dump())
    return {"id": student_id}

@router.get("/", response_model=list)
async def list_students_api(country: str = None, age: int = None):
    filters = {}
    if country:
        filters["address.country"] = country
    if age:
        filters["age"] = {"$gte": age}
    return await get_students(filters)

@router.get("/{id}", response_model=dict)
async def fetch_student_api(id: str):
    student = await get_student_by_id(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.patch("/{id}", status_code=204)
async def update_student_api(id: str, student: StudentUpdate):
    updated = await update_student(id, student.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")

@router.delete("/{id}", status_code=200)
async def delete_student_api(id: str):
    deleted = await delete_student(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")