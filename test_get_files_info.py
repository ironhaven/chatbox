import functions
from functions.get_files_info import get_files_info


print("Reading working directory")
print(get_files_info("calculator", "."))

print("Reading pkg")
print(get_files_info("calculator", "pkg"))
print("Reading /bin")
print(get_files_info("calculator", "/bin"))
print("Reading ../")
print(get_files_info("calculator", "../"))
print("Reading main.py")
print(get_files_info("calculator", "main.py"))
