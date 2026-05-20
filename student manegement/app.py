import json
import os

class Student:
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        return {"id": self.student_id, "name": self.name, "grade": self.grade}


class StudentManager:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    for s_id, info in data.items():
                        self.students[s_id] = Student(s_id, info['name'], info['grade'])
            except json.JSONDecodeError:
                print("Warning: Data file corrupted. Starting with an empty database.")

    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump({s_id: s.to_dict() for s_id, s in self.students.items()}, f, indent=4)

    def add_student(self, student_id, name, grade):
        if student_id in self.students:
            print(f"❌ Error: Student ID {student_id} already exists!")
            return False
        self.students[student_id] = Student(student_id, name, grade)
        self.save_data()
        print(f"✅ Student '{name}' added successfully.")
        return True

    def update_student(self, student_id, name=None, grade=None):
        if student_id not in self.students:
            print(f"❌ Error: Student ID {student_id} not found.")
            return False
        if name:
            self.students[student_id].name = name
        if grade:
            self.students[student_id].grade = grade
        self.save_data()
        print(f"✅ Student ID {student_id} updated successfully.")
        return True

    def delete_student(self, student_id):
        if student_id in self.students:
            removed = self.students.pop(student_id)
            self.save_data()
            print(f"✅ Student '{removed.name}' removed successfully.")
            return True
        print(f"❌ Error: Student ID {student_id} not found.")
        return False

    def list_students(self):
        if not self.students:
            print("\n--- No records found ---")
            return
        print("\n" + "="*40)
        print(f"{'ID':<10} | {'Name':<20} | {'Grade':<5}")
        print("="*40)
        for s in self.students.values():
            print(f"{s.student_id:<10} | {s.name:<20} | {s.grade:<5}")
        print("="*40)


def main():
    manager = StudentManager()
    
    while True:
        print("\n=== Student Management System ===")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. List All Students")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            s_id = input("Enter Student ID: ").strip()
            if not s_id: 
                print("ID cannot be empty.")
                continue
            name = input("Enter Name: ").strip()
            grade = input("Enter Grade: ").strip()
            manager.add_student(s_id, name, grade)
            
        elif choice == '2':
            s_id = input("Enter Student ID to update: ").strip()
            name = input("Enter new Name (leave blank to skip): ").strip()
            grade = input("Enter new Grade (leave blank to skip): ").strip()
            manager.update_student(s_id, name if name else None, grade if grade else None)
            
        elif choice == '3':
            s_id = input("Enter Student ID to delete: ").strip()
            manager.delete_student(s_id)
            
        elif choice == '4':
            manager.list_students()
            
        elif choice == '5':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()