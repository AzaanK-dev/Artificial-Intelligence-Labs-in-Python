# I. a Python program to square and cube every number in a given list of integers using Lambda.

l = [12,23,41,52,10]

for x in l:
    square = lambda x: x**2
    print(square(x))

for x in l:
    cube = lambda x: x**3
    print(cube(x))



# II. a Python program to find if a given string starts with a given character using Lambda

str = "hello, this is me"
char = "h"
isStart = lambda str, char: str.startswith(char)
print(isStart(str,char))



# III. a Python program to extract year, month, date and time using Lambda.

from datetime import datetime
date = datetime.now()

year = lambda d: d.year
month = lambda d: d.month
day = lambda d: d.day
time = lambda d: d.time

print(year(date))
print(month(date))
print(day(date))
print(time(date))