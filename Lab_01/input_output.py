# (i) Write a Python program to swap 4 variables values (input four values).

def swap_variables(a, b, c, d):
    print("Before swapping:")
    print(f"a = {a}, b = {b}, c = {c}, d = {d}")

    # Swapping values
    a, b, c, d = d, c, b, a

    print("After swapping:")
    print(f"a = {a}, b = {b}, c = {c}, d = {d}")

swap_variables(2, 56, 78, 9)



# (ii) Write a Python program to convert temperatures to and from celsius, fahrenheit.

def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius / 5) * 9 + 32
    return fahrenheit

def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5 / 9
    return celsius

input_temp = float(input("Enter the temperature: "))
unit = input("Enter the unit (C for Celsius, F for Fahrenheit): ").upper()

if unit == 'C':
    converted_temp = celsius_to_fahrenheit(input_temp)
    print(f"{input_temp}°C is equal to {converted_temp}°F")
elif unit == 'F':
    converted_temp = fahrenheit_to_celsius(input_temp)
    print(f"{input_temp}°F is equal to {converted_temp}°C")
else:
    print("Invalid unit. Please enter 'C' for Celsius or 'F' for Fahrenheit.")
