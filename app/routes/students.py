from fastapi import APIRouter, HTTPException
from app.schemas import StudentCreate, StudentUpdate
from app.services.students import create_student, get_students, get_student_by_id, update_student, delete_student
from bson import ObjectId
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/", response_model=dict, status_code=201)
async def create_student_endpoint(student: StudentCreate):
    """
    Create a new student.
    """
    try:
        student_id = await create_student(student.model_dump())
        return JSONResponse(content={"message": "Student created successfully.", "id": student_id}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating student: {str(e)}")


@router.get("/", response_model=list)
async def list_students(country: str = None, age: int = None):
    """
    List students with optional filters.
    """
    filters = {}
    if country:
        filters["address.country"] = country
    if age:
        filters["age"] = {"$gte": age}

    students = await get_students(filters)
    return JSONResponse(content={"students": students}, status_code=200)


@router.get("/{id}", response_model=dict)
async def fetch_student(id: str):
    """
    Fetch a student by ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail=f"'{id}' is not a valid ObjectId.")
    student = await get_student_by_id(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return JSONResponse(content=student, status_code=200)


@router.patch("/{id}", response_model=dict, status_code=200)
async def update_student_endpoint(id: str, student: StudentUpdate):
    """
    Update student details.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail=f"'{id}' is not a valid ObjectId.")
    
    update_data = student.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided to update.")

    update_result = await update_student(id, update_data)

    if update_result is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    if update_result.matched_count == 1 and update_result.modified_count == 0:
        return JSONResponse(
            content={"message": f"No changes made as the provided data is identical to the existing information.\n{update_data}"},
            status_code=200,
        )

    return JSONResponse(content={"message": "Student updated successfully."}, status_code=200)


@router.delete("/{id}", response_model=dict, status_code=200)
async def delete_student_endpoint(id: str):
    """
    Delete a student by ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail=f"'{id}' is not a valid ObjectId.")
    deleted = await delete_student(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found.")
    return JSONResponse(content={"message": "Student deleted successfully."}, status_code=200)
