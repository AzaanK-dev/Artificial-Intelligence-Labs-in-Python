# (i) Write a list comprehension which, from a list, generates a lowercased version of each string that has a length greater than five

words = ['Python', 'University', 'Karachi', 'Lab', 'Computer', 'AI']

result = [word.lower() for word in words if len(word) > 5]

print("Original list:", words)
print("Result:", result)



# (ii) Program to remove the 0th, 4th and 5th elements

sample_list = ['Red', 'Green', 'White', 'Black', 'Pink', 'Yellow', 'Teapink']

result = [value for index, value in enumerate(sample_list) if index not in (0, 4, 5)]

print("Original list:", sample_list)
print("After removing:", result)