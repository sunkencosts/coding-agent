from functions.write_files import write_file


print ("Writing file")
result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print(result1)
print ("Writing file")
result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print(result2)
print ("Writing file")
result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print(result3)