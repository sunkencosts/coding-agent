from functions.get_file_contents import get_file_content

print ("Getting file content")
result1 = get_file_content("calculator", "lorem.txt")
print(f"content length is: {len(result1)}")

print ("getting main.py content")
result2=get_file_content("calculator", "main.py")
print(result2)


print ("getting pkg/calculator.py content")
result3= get_file_content("calculator", "pkg/calculator.py")
print(result3)
print("should return an error")
result3 = get_file_content("calculator", "/bin/cat")
print(result3)


print("should return an error")
result4=get_file_content("calculator", "pkg/does_not_exist.py")
print(result4)