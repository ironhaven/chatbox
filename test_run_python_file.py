import functions
from functions.run_python_file import run_python_file


print("run main.py")
print(run_python_file("calculator", "main.py"))
print("run main.py 3 + 5")
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print("run tests.py")
print(run_python_file("calculator", "tests.py"))
print("run ../main.py")
print(run_python_file("calculator", "../main.py"))
print("run nonexistent.py")
print(run_python_file("calculator", "nonexistent.py"))
print("run lorem.txt")
print(run_python_file("calculator", "lorem.txt"))
