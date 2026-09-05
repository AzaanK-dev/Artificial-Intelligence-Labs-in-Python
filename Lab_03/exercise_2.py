# Write a python program to accept the data for a no of cities and store it in a file.

inp = int(input("No. of cities you want to enter: "))

if inp>=1:
    file = open("city_info.txt","a")
    for i in range(0,inp):
        city = input("City Name: ")
        population = input("Population: ")
        mayor = input("Mayor Name: ")
        file.write(f"City Name: {city} | Population: {population} | Mayor Name: {mayor}\n")

    file.close()
else:
    print("Invalid input")



# Write a python program to create a data file student.txt and append the message “Now we are AI students”s 

f = open("student.txt","a")
f.write("Now we are AI students")
f.close()

