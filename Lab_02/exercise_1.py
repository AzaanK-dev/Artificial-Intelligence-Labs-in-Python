# (I) Make a program that takes inputs like height, width and depth, find volume & compare it with ranges and print the label

height = float(input("Enter height: "))
width = float(input("Enter width: "))
depth = float(input("Enter depth: "))

volume = height * width * depth

if volume >= 1 and volume <= 10:
    print("Extra Small")
elif volume <= 25:
    print("Small")
elif volume <= 75:
    print("Medium")
elif volume <= 100:
    print("Large")
elif volume <= 250:
    print("Extra Large")
elif volume >= 251:
    print("Extra-Extra Large")
else:
    print("Invalid")



# (II) In a company ,worker efficiency is determined on the basis of the time required for a worker to complete a particular job.If the  time taken by the worker is between 2-3 hours then the worker is said to be highly efficient. If the time required by the worker is between 3-4hours,then the worker is ordered to improve speed. If the time taken is between 4-5 hours ,the worker is given training to improve his speed ,and if the time taken by the worker is more than 5 hours ,then the worker  haas to leave the company, If the time taken by the worker is input through the keyboard,find the efficiency of the worker.

time_taken = float(input("Enter no. of hrs: "))

if time_taken >= 2 and time_taken <= 3:
    print("highly efficient.")
elif time_taken > 3 and time_taken <= 4:
    print("ordered to improve speed.")
elif time_taken > 4 and time_taken <= 5:
    print("given training to improve his speed.")
else:
    print("leave the company.")



# (iii)The program must prompt the user for a username and password. The program should compare the password given by the user to a known password. If the password matches, the program should display “Welcome!” If it doesn’t match, the program should display “I don’t know you. 

username = input("Enter username: ")
password = input("Enter password: ")

if password == "abc$123" or password == "ABC$123":
    print("Welcome!")
else:
    print("I don't know you.")
