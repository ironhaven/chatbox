import functions
from functions.write_file import write_file


print("write lorem")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print("write morelorem")
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print("write /tmp")
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
