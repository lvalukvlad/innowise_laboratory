def calculate_average(grades):
    """Вычисление среднего значения оценок."""
    if not grades:
        return None
    return sum(grades) / len(grades)

def add_student(students):
    """Добавление студента в список."""
    name = input("Enter student name: ").strip()
    for student in students:
        if student["name"].lower() == name.lower():
            print(f"Student '{name}' already exists!")
            return
    new_student = {"name": name, "grades": []}
    students.append(new_student)
    print(f"Student '{name}' added successfully!")

def add_grades(students):
    """Добавление оценки существующему студенту."""
    if not students:
        print("No students available. Please add students first.")
        return
    name = input("Enter student name: ").strip()
    student_found = None
    for student in students:
        if student["name"].lower() == name.lower():
            student_found = student
            break
    if not student_found:
        print(f"Student '{name}' not found!")
        return
    print(f"Adding grades for {student_found['name']}:")
    while True:
        try:
            grade_input = input("Enter a grade (or 'done' to finish): ").strip()

            if grade_input.lower() == 'done':
                break

            grade = int(grade_input)

            if 0 <= grade <= 100:
                student_found["grades"].append(grade)
                print(f"Grade {grade} added successfully!")
            else:
                print("Invalid grade! Please enter a number between 0 and 100.")

        except ValueError:
            print("Invalid input! Please enter a number or 'done'.")


def show_report(students):
    """Генерация отчёта о студентах."""
    if not students:
        print("No students available.")
        return
    print("\n--- Student Report ---")
    averages = []
    valid_students = 0
    for student in students:
        avg = calculate_average(student["grades"])
        if avg is not None:
            print(f"{student['name']}'s average grade is {avg:.1f}.")
            averages.append(avg)
            valid_students += 1
        else:
            print(f"{student['name']}'s average grade is N/A.")
    if not averages:
        print("No grades available for any student.")
        return
    print("-" * 25)
    print(f"Max Average: {max(averages):.1f}")
    print(f"Min Average: {min(averages):.1f}")
    print(f"Overall Average: {sum(averages) / len(averages):.1f}")

def find_top_performer(students):
    """Поиск лучшего студента по баллу."""
    if not students:
        print("No students available.")
        return
    students_with_grades = []
    for student in students:
        avg = calculate_average(student["grades"])
        if avg is not None:
            students_with_grades.append((student, avg))
    if not students_with_grades:
        print("No students with grades available.")
        return
    top_student, top_avg = max(students_with_grades, key=lambda x: x[1])
    print(f"The student with the highest average is {top_student['name']} with a grade of {top_avg:.1f}.")


def main():
    students = []
    while True:
        print("\n--- Student Grade Analyzer ---")
        print("1. Add a new student")
        print("2. Add grades for a student")
        print("3. Generate a full report")
        print("4. Find top student")
        print("5. Exit program")
        try:
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                add_student(students)
            elif choice == '2':
                add_grades(students)
            elif choice == '3':
                show_report(students)
            elif choice == '4':
                find_top_performer(students)
            elif choice == '5':
                print("Exiting program.")
                break
            else:
                print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()