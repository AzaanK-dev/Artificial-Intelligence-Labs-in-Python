# (i) Common List Methods:

lst = [10, 20, 30]

lst.append(40)
print(lst)

lst.insert(1, 15)
print(lst)

lst.remove(20)
print(lst)

lst.reverse()
print(lst)

lst.sort()
print(lst)




# (ii) Program to count strings whose first and last characters are the same

sample_list = ['abc', 'xyz', 'aba', '1221']
count = 0

for string in sample_list:
    if len(string) >= 2 and string[0] == string[-1]:
        count += 1

print("Number of strings:", count)