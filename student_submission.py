# Student Name: Evelyn Idogbe
# Student ID: A00050322

import datetime
from tabulate import tabulate

# ------------------------
# Validation Functions
# ------------------------

def validate_student_id(student_id):
    """Validate student ID is a 2-digit number"""
    return student_id.isdigit() and len(student_id) == 2

def validate_dob(dob):
    """Validate date of birth is in YYYY-MM-DD format"""
    try:
        datetime.datetime.strptime(dob, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_score(score):
    """Validate score is an integer between 0 and 100"""
    try:
        score_value = int(score)
        return 0 <= score_value <= 100
    except ValueError:
        return False

# ------------------------
# Core Functionality
# ------------------------

def calculate_overall_score(scores):
    """Calculate the average of all scores"""
    return sum(scores) / len(scores)

def determine_category(score):
    """Determine grade category based on score"""
    if score >= 70:
        return "First"
    elif score >= 60:
        return "Upper First"  # Changed from Upper-First to match expected output
    elif score >= 50:
        return "2:1"  # Changed from Second to 2:1 to match expected output
    else:
        return "Third"

def round_to_category(score):
    """Round score to nearest category boundary"""
    if score >= 72:
        return 75, "First"
    elif score >= 68:
        return 72, "Upper First"  # Changed from Upper-First to match expected output
    elif score >= 50:
        return 68, "2:1"  # Changed from Second to 2:1 to match expected output
    else:
        return 50, "Third"

def calculate_age(dob):
    """Calculate age based on date of birth"""
    try:
        birth_date = datetime.datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    except ValueError:
        print(f"⚠ Error calculating age: Invalid date format '{dob}'")
        return 0

# ------------------------
# Input Function
# ------------------------

def get_student_data():
    """Collect student data from user input"""
    student_list = []
    
    while True:
        student_id = input("Enter student ID (or 'end' to stop): ").strip()
        
        if student_id.lower() == "end":
            break
            
        if not validate_student_id(student_id):
            print("⚠ Invalid input! Student ID must be a 2-digit number.")
            continue
            
        name = input("Enter student's name: ").strip()
        dob = input("Enter student's D.o.B (YYYY-MM-DD): ").strip()
        
        if not validate_dob(dob):
            print("⚠ Invalid input! Date format should be YYYY-MM-DD.")
            continue
            
        scores = []
        valid_inputs = True
        
        # Collect 4 scores
        for i in range(4):
            score_input = input(f"Coursework {i + 1} score: ").strip()
            
            if not validate_score(score_input):
                print("⚠ Invalid input! Please enter a valid integer for the scores.")
                valid_inputs = False
                break
                
            scores.append(int(score_input))
            
        if valid_inputs:
            student_list.append((student_id, name, dob, scores))
            
            # If we have collected 3 students, break out of the loop
            if len(student_list) >= 3:
                break
                
    return student_list

# ------------------------
# Display and Save
# ------------------------

def display_results(students):
    """Display formatted student results"""
    sorted_students = sorted(students, key=lambda x: x["ID"])
    headers = ["UID", "Name", "D.o.B", "Age", "Raw Score", "Rounded Score", "Category"]
    table = [[
        s["ID"],
        s["Name"],
        s["D.o.B"],
        s["Age"],
        round(s["Score"], 1),  # Changed to round to 1 decimal place
        s["Rounded Score"],
        s["Category"]
    ] for s in sorted_students]
    
    print("\n📊 Student Summary:\n")
    print(tabulate(table, headers=headers))

def save_results_to_file(students):
    """Save student results to a file"""
    with open("students.txt", "w") as file:
        file.write("UID Name D.o.B Age RawScore RoundedScore Category\n")
        for s in students:
            file.write(f"{s['ID']} {s['Name']} {s['D.o.B']} {s['Age']} {round(s['Score'], 1)} {s['Rounded Score']} {s['Category']}\n")
    
    print("✅ Student data saved to students.txt")

# ------------------------
# Advanced Functions
# ------------------------

def advanced(filename, weights=None):
    """Process student data from a file with optional component weights"""
    if weights is None:
        weights = [25, 25, 25, 25]  # Default equal weights if none provided
        
    # Ensure weights sum to 100
    if abs(sum(weights) - 100) > 0.01:
        print("⚠ Error: Weights must sum to 100%")
        return
        
    students = []
    
    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split(",")
            if len(parts) < 7:  # ID, name, DOB, and at least 4 scores
                continue
                
            student_id, name, dob = parts[0], parts[1], parts[2]
            scores = [int(score) for score in parts[3:7]]  # Take first 4 scores
            
            # Apply weights
            weighted_score = sum(score * weight / 100 for score, weight in zip(scores, weights))
            rounded_score, category = round_to_category(weighted_score)
            age = calculate_age(dob)

            students.append({
                "ID": student_id,
                "Name": name,
                "D.o.B": dob,
                "Age": age,
                "Score": weighted_score,
                "Rounded Score": rounded_score,
                "Category": category
            })

        display_results(students)
        save_results_to_file(students)

    except FileNotFoundError:
        print(f"⚠ File not found: {filename}")
    except Exception as e:
        print(f"⚠ Error processing file: {str(e)}")

def setup_module():
    """Setup module information and assessment components"""
    try:
        module_name = input("Enter module name: ").strip()
        
        while True:
            try:
                num_components = int(input("How many assessment components? "))
                if num_components <= 0:
                    print("⚠ Number of components must be positive.")
                    continue
                break
            except ValueError:
                print("⚠ Please enter a valid number.")
        
        weights = []
        for i in range(num_components):
            comp_name = input(f"Component {i+1} name: ")
            
            while True:
                try:
                    comp_weight = float(input(f"Component {i+1} weight (%): "))
                    weights.append(comp_weight)
                    break
                except ValueError:
                    print("⚠ Please enter a valid weight percentage.")
        
        # Check if weights sum to 100%
        if abs(sum(weights) - 100) > 0.01:
            print("⚠ Error: Weights must sum to 100%. Please try again.")
            return None
            
        print(f"✅ Module '{module_name}' setup complete.")
        return weights
        
    except Exception as e:
        print(f"⚠ Error in setup: {str(e)}")
        return None

# ------------------------
# Main Entry
# ------------------------

def main():
    """Main function to run the application"""
    print("🎓 Welcome to the Student Grading System\n")
    
    try:
        # Ask whether to run advanced mode
        mode = input("Would you like to use advanced mode? (y/n): ").strip().lower()
        
        if mode == 'y':
            # Setup module and weights
            weights = setup_module()
            if weights:
                filename = input("Enter student data filename: ").strip()
                advanced(filename, weights)
            else:
                print("⚠ Module setup failed. Running in standard mode.")
                process_standard_input()
        else:
            process_standard_input()
            
    except Exception as e:
        print(f"⚠ An unexpected error occurred: {str(e)}")

def process_standard_input():
    """Process student data from standard input"""
    student_data = get_student_data()
    students = []

    for student_id, name, dob, scores in student_data:
        score = calculate_overall_score(scores)
        rounded_score, category = round_to_category(score)
        age = calculate_age(dob)

        students.append({
            "ID": student_id,
            "Name": name,
            "D.o.B": dob,
            "Age": age,
            "Score": score,
            "Rounded Score": rounded_score,
            "Category": category
        })

    display_results(students)
    save_results_to_file(students)

if _name_ == "_main_":
    main()
