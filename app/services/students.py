from app.db import db
from app.models import student_helper
from bson import ObjectId
import traceback
from typing import List,Dict,Union

async def create_student(data: Dict) -> Union[str,Dict]:
    try:
        student = await db["students"].insert_one(data)
        print(f"Successfully created student object > {student}")
        return str(student.inserted_id)
    except Exception as e:
        print(traceback.format_exception(e))
        return {"error":"Internal sserver error"}

async def get_students(filter: Dict) -> Union[List,Dict]:
    try:
        students = await db["students"].find(filter).to_list(100)
        print(f"Successfully fetched data > {len(students)}")
        return [student_helper(student) for student in students]
    except Exception as e:
        print(traceback.format_exception(e))
        return {"error":"Internal sserver error"}
    
async def get_student_by_id(student_id: str) -> Dict:
    try:
        student = await db["students"].find_one({"_id": ObjectId(student_id)})
        print(f"Successfully fetched id > {student_id}")
        return student_helper(student) if student else None
    except Exception as e:
        print(traceback.format_exception(e))
        return {"error":"Internal sserver error"}


async def update_student(student_id: str, data: Dict) -> Union[bool,Dict]:
    try:
        
        result = await db["students"].update_one({"_id": ObjectId(student_id)}, {"$set": data})

        # print(f"Successfully modified data for id > {student_id}, data > {data}")

        return result
    except Exception as e:
        print(traceback.format_exception(e))
        return {"error":"Internal sserver error"}


async def delete_student(student_id: str) -> Union[bool,Dict]:
    try:
        result = await db["students"].delete_one({"_id": ObjectId(student_id)})
        print(f"Successfully Deletd data for id> {student_id}")
        return result.deleted_count > 0
    except Exception as e:
        print(traceback.format_exception(e))
        return {"error":"Internal sserver error"}

