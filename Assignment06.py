# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: Course registration using functions, classes, JSON, and structured error handling.
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Starter Script
#   Theresa Dryden,11/11/2026,Organized script into classes and static methods
# ------------------------------------------------------------------------------------------ #
import json

MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:
    1. Register a Student for a Course
    2. Show current data
    3. Save data to a file
    4. Exit the program
-----------------------------------------
'''
FILE_NAME: str = "Enrollments.json"
menu_choice: str = ''
students: list = []


class IO:
    """Handle all console input, output, and error messages."""

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """Display a friendly error message and optional technical details."""
        print(f"Error: {message}")
        if error is not None:
            print("-- Technical Error Message --")
            print(type(error).__name__, str(error), sep=": ")

    @staticmethod
    def output_menu(menu: str):
        """Display the supplied menu text."""
        print(menu)

    @staticmethod
    def input_menu_choice():
        """Ask the user to select a menu option and return it as text."""
        return input("What would you like to do: ").strip()

    @staticmethod
    def output_student_courses(student_data: list):
        """Display every enrollment as comma-separated values."""
        print("-" * 50)
        for student in student_data:
            print(f'{student["FirstName"]},{student["LastName"]},'
                  f'{student["CourseName"]}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """Validate a student's name and append a course registration."""
        try:
            first_name = input("Enter the student's first name: ").strip()
            if not first_name.isalpha():
                raise ValueError("The first name must contain letters only.")
            last_name = input("Enter the student's last name: ").strip()
            if not last_name.isalpha():
                raise ValueError("The last name must contain letters only.")
            course_name = input("Please enter the name of the course: ").strip()
            if not course_name:
                raise ValueError("The course name cannot be empty.")
            student_data.append({"FirstName": first_name,
                                 "LastName": last_name,
                                 "CourseName": course_name})
            print(f"You have registered {first_name} {last_name} "
                  f"for {course_name}.")
        except ValueError as error:
            IO.output_error_messages("Invalid student data.", error)
        except Exception as error:
            IO.output_error_messages("Unable to register the student.", error)


class FileProcessor:
    """Handle reading and writing enrollment data in JSON format."""

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """Read saved enrollments and populate the supplied list."""
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                loaded_data = json.load(file)
            if not isinstance(loaded_data, list):
                raise ValueError("The JSON file must contain a list.")
            for student in loaded_data:
                if not isinstance(student, dict) or not all(
                        key in student for key in
                        ("FirstName", "LastName", "CourseName")):
                    raise ValueError("An enrollment has missing fields.")
            student_data.extend(loaded_data)
        except FileNotFoundError as error:
            IO.output_error_messages("Enrollment file was not found.", error)
        except (ValueError, json.JSONDecodeError) as error:
            IO.output_error_messages("Enrollment file has invalid data.", error)
        except Exception as error:
            IO.output_error_messages("Unable to read enrollment file.", error)

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """Save enrollments as formatted JSON and display saved records."""
        try:
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(student_data, file, indent=2)
            print("The following data was saved to file!")
            IO.output_student_courses(student_data)
        except (OSError, TypeError, ValueError) as error:
            IO.output_error_messages("Unable to save enrollment data.", error)
        except Exception as error:
            IO.output_error_messages("Unexpected error while saving.", error)


# Main body: coordinate tasks without duplicating their implementation.
def main():
    """Load enrollments and run the course-registration menu."""
    students: list = []
    menu_choice: str = ''
    FileProcessor.read_data_from_file(FILE_NAME, students)
    while True:
        IO.output_menu(MENU)
        menu_choice = IO.input_menu_choice()
        if menu_choice == "1":
            IO.input_student_data(students)
        elif menu_choice == "2":
            IO.output_student_courses(students)
        elif menu_choice == "3":
            FileProcessor.write_data_to_file(FILE_NAME, students)
        elif menu_choice == "4":
            break
        else:
            print("Please only choose option 1, 2, 3, or 4.")
    print("Program Ended")


if __name__ == "__main__":
    main()
