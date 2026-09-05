# Student Grade Management System

student_list = []   # list
subjects = ("English", "Math", "Urdu")  # tupple


def add_student():
    print("\n--- Add Student ---")
    name = input("Enter student name: ")
    id = input("Enter student ID: ")
    student = {      # dictionary
        "name": name,
        "id": id,
        "marks": {}
    }
    print("\nEnter marks out of 100:")

    for subject in subjects:
        while True:
            try:
                marks = float(input(f"Enter {subject} marks: "))
                if 0 <= marks <= 100:
                    student["marks"][subject] = marks
                    break
                else:
                    print("Marks must be between 0 and 100.")

            except ValueError:
                print("Please enter a valid number.")
    
    student_list.append(student)
    print(f"\nStudent {name} with ID {id} added successfully.")
   

def view_students():
    print("\nList of Students -----")

    if not student_list:
        print("No students found.")
    else:
        for student in student_list:
            print(f"\nName: {student['name']}")
            print(f"ID: {student['id']}")
            print("Marks:")
            for subject in subjects:
                print(f"{subject}: {student['marks'][subject]}")


def calculate_grades():
    print("\n--- Calculate Grades ---")
    id = input("Enter student ID: ")
    found = False

    for student in student_list:
        if student["id"] == id:
            total = student["marks"]["English"] + \
                    student["marks"]["Math"] + \
                    student["marks"]["Urdu"]

            percentage = (total / 300) * 100
            if percentage >= 90:
                grade = "A"
            elif percentage >= 80:
                grade = "B"
            elif percentage >= 70:
                grade = "C"
            elif percentage >= 60:
                grade = "D"
            else:
                grade = "F"

            print(f"\nStudent Name: {student['name']}")
            print(f"Student ID: {student['id']}")
            print(f"Total Marks: {total}/300")
            print(f"Percentage: {percentage:.2f}%")
            print(f"Grade: {grade}")
            found = True
            break
    if not found:
        print("Student not found.")


def search_student():
    print("\n--- Search Student ---")
    search_id = input("Enter student ID to search: ")
    found = False
    for student in student_list:
        if student["id"] == search_id:
            print("\nStudent found!")
            print(f"Name: {student['name']}")
            print(f"ID: {student['id']}")
            print("Marks:")
            for subject in subjects:
                print(f"{subject}: {student['marks'][subject]}")

            found = True
            break

    if not found:
        print("Student not found.")



def main():

    while True:
        print("\n==============================")
        print(" STUDENT GRADE MANAGEMENT")
        print("==============================")
        print("1. Add Student")
        print("2. View Students")
        print("3. Calculate/Display Grades")
        print("4. Search for Student")
        print("5. Exit")
        print("==============================")

        choice = input("Choose an option (1-5): ")
        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            calculate_grades()
        elif choice == "4":
            search_student()
        elif choice == "5":
            print("\nExiting the program.")
            print("Thank you for using the Student Grade Management System!")
            break
        else:
            print("Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    main()