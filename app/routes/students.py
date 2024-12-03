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
        response = await create_student(student.model_dump())
        # error
        if isinstance(response,dict) and 'error' in response:
            return JSONResponse(status_code=500,content=response)
        # id
        return JSONResponse(content={"id": response}, status_code=201)
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

    response = await get_students(filters)
    # error
    if isinstance(response,dict) and 'error' in response:
        return JSONResponse(status_code=500,content=response)
    # students
    return JSONResponse(content=response, status_code=200)


@router.get("/{id}", response_model=dict)
async def fetch_student(id: str):
    """
    Fetch a student by ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail=f"'{id}' is not a valid ObjectId.")
    response = await get_student_by_id(id)
    # error
    if isinstance(response,dict) and 'error' in response:
        return JSONResponse(status_code=500,content=response)
    # students
    if not response:
        raise HTTPException(status_code=404, detail="Student not found.")
    return JSONResponse(content=response, status_code=200)


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
    # error
    if isinstance(update_result,dict) and 'error' in update_result:
            return JSONResponse(status_code=500,content=update_result)

    if update_result is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    if update_result.matched_count == 1 and update_result.modified_count == 0:
        return JSONResponse(
            content={"message": f"No changes made as the provided data is identical to the existing information.\n{update_data}"},
            status_code=200,
        )

    # return JSONResponse(content={"message": "Student updated successfully."}, status_code=200)


@router.delete("/{id}", response_model=dict, status_code=200)
async def delete_student_endpoint(id: str):
    """
    Delete a student by ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail=f"'{id}' is not a valid ObjectId.")
    deleted = await delete_student(id)
    # error
    if isinstance(deleted,dict) and 'error' in deleted:
        return JSONResponse(status_code=500,content=deleted)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found.")
    return JSONResponse(content={"message": "Student deleted successfully."}, status_code=200)
