# (ii) Make a program that lists the countries in the set
clist = ['Canada','USA','Mexico','Australia'] 
for c in clist:
    print(c)


# (ii) 1. Create a loop that counts from 0 to 100
for i in range(101):
    print(i)

# 2. Make a multiplication table using a loop
for i in range(1, 11):
    for j in range(1, 11):
        print(f"{i} x {j} = {i * j}")
    print()  

# 3. Output the numbers 1 to 10 backwards using a loop
for i in range(10, 0, -1):    # runs -1 step
    print(i)

# 4. Create a loop that counts all even numbers to 10 
for i in range(2, 11, 2):   # runs 2 step 
    print(i)

# 5. Create a loop that sums the numbers from 100 to 200
total = 0 
for i in range(100, 201):
    total += i
print(total)




# (iii) 1.  Make a program that lists the countries in the set below using a while loop.
clist = ["Canada","USA","Mexico"] 
c = 0
while c < len(clist):
    print(clist[c])
    c += 1

