app_files = ['__init__.py','main.py','config.py','models.py','schemas.py','routes/__init__.py','routes/students.py','services/__init__.py',
             'services/students.py','db.py']
main_files = ['.env','requirements.txt','Dockerfile','.dockerignore','ReadME.md','.gitignore']
test_files = ['__init__.py','test_student.py']

import os

if not os.path.exists('app'):
    os.makedirs('app')
if not os.path.exists('tests'):
    os.makedirs('tests')

for file in app_files:
    if '/' in file:
        sub_dir = f"app/{file.rsplit('/', 1)[0]}"  
        file_name = file.rsplit('/', 1)[1]  
        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)
        file_path = f"{sub_dir}/{file_name}"
    else:
        file_path = f"app/{file}"
    
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass
        print(f"Created: {file_path}")

for file in main_files:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            pass
        print(f"Created: {file}")

for file in test_files:
    file_path = f"tests/{file}"
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass
        print(f"Created: {file_path}")

print("Project structure has been created successfully.")


