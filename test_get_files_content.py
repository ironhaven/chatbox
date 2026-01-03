import functions
from functions.get_file_content import get_file_content


print("Reading lorem")
content = get_files_content("calculator", "lorem.txt")
print(content[-100:])
assert content.endswith(" characters]")
print("Reading main.py")
print(get_files_content("calculator", "main.py")[:500])
print("Reading calculator.py")
print(get_files_content("calculator", "pkg/calculator.py")[:1500])
print("Reading /bin")
print(get_files_content("calculator", "/bin/cat"))
print("Reading nonexistant")
print(get_files_content("calculator", "pgk/does_not_exist.py"))
