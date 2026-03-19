from functions.run_python_file import run_python_file

print("Running main")
result1 = run_python_file("calculator", "main.py")
print(result1)

result2 = run_python_file("calculator", "main.py", ["3 + 5"])
print (result2)

result3 = run_python_file("calculator", "tests.py")
print (result3)
print("Should error")
result4 = run_python_file("calculator", "../main.py")
print (result4)
print("Should error")
result5 = run_python_file("calculator", "nonexistent.py")
print (result5)
print("Should error")
result6 = run_python_file("calculator", "lorem.txt")
print (result6)