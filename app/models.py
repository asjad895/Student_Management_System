from typing import Dict

def student_helper(student) -> Dict:
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"],
        "address": student["address"],
    }
