# (i) Common Dictionary Methods:

student = {
    "name": "Ali",
    "age": 20,
    "department": "Computer Science"
}

print("Name:", student.get("name"))
print("Keys:", student.keys())
print("Values:", student.values())
print("Items:", student.items())

student.update({"age": 21})
print("After update:", student)

student.pop("age")
print("After pop:", student)

student.clear()
print("After clear:", student)




# (ii) Program to concatenate three dictionaries

dic1 = {1: 10, 2: 20}
dic2 = {3: 30, 4: 40}
dic3 = {5: 50, 6: 60}

new_dictionary = {}

new_dictionary.update(dic1)
new_dictionary.update(dic2)
new_dictionary.update(dic3)

print("Concatenated dictionary:", new_dictionary)