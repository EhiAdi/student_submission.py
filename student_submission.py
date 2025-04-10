import datetime
from tabulate import tabulate

def calculate_overall_score(scores, weights=None):
    """
    Calculate the overall score based on component scores and weights.
    
    Args:
        scores (list): List of component scores
        weights (list, optional): List of weights for each component. If None, equal weights are used.
        
    Returns:
        float: The calculated overall score
    """
    if weights is None:
        # Default to equal weights if not provided
        weights = [0.25, 0.25, 0.25, 0.25]
    
    # Ensure weights sum to 1
    total_weight = sum(weights)
    if total_weight != 1:
        weights = [w / total_weight for w in weights]
    
    # Calculate weighted sum
    overall_score = sum(score * weight for score, weight in zip(scores, weights))
    return overall_score

def determine_category(score):
    """
    Determine the category based on the overall score.
    
    Args:
        score (float): The overall score
        
    Returns:
        str: The category
    """
    if score >= 85:
        return "Upper-First"
    elif score >= 72:
        return "First"
    elif score >= 68:
        return "2:1"
    elif score >= 60:
        return "2:2"
    elif score >= 52:
        return "Third"
    elif score >= 40:
        return "Pass"
    else:
        return "Fail"

def round_to_category(score):
    """
    Rounds a score to the nearest category boundary.
    
    Args:
        score (float or int): The numerical score to round
        
    Returns:
        tuple: (rounded_score, category)
    """
    # Define category boundaries
    boundaries = {
        85: "Upper-First",
        72: "First",
        68: "2:1",
        60: "2:2",
        52: "Third",
        40: "Pass",
        0: "Fail"
    }
    
    # Sort boundaries for processing
    sorted_boundaries = sorted(boundaries.keys())
    
    # Handle edge cases
    if score >= sorted_boundaries[-1]:
        return (sorted_boundaries[-1], boundaries[sorted_boundaries[-1]])
    if score <= sorted_boundaries[0]:
        return (sorted_boundaries[0], boundaries[sorted_boundaries[0]])
    
    # Find the two nearest boundaries
    lower_bound = None
    upper_bound = None
    
    for boundary in sorted_boundaries:
        if boundary <= score:
            lower_bound = boundary
        if boundary > score and upper_bound is None:
            upper_bound = boundary
    
    # Calculate distances to boundaries
    distance_to_lower = score - lower_bound
    distance_to_upper = upper_bound - score
    
    # Round to nearest boundary (round up if exactly halfway)
    if distance_to_lower <= distance_to_upper:
        return (lower_bound, boundaries[lower_bound])
    else:
        return (upper_bound, boundaries[upper_bound])

def validate_student_id(student_id, existing_ids=None):
    """
    Validate student ID.
    
    Args:
        student_id (str): The student ID to validate
        existing_ids (list, optional): List of existing IDs to check for duplicates
        
    Returns:
        bool: True if valid, False otherwise
    """
    if student_id.lower() == "end":
        return True
    
    if not student_id.isdigit():
        return False
    
    if len(student_id) != 2:
        return False
    
    if existing_ids and student_id in existing_ids:
        return False
    
    return True

def validate_dob(dob):
    """
    Validate date of birth in ISO format (YYYY-MM-DD).
    
    Args:
        dob (str): The date of birth to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        year, month, day = dob.split('-')
        datetime.datetime(int(year), int(month), int(day))
        return True
    except (ValueError, TypeError):
        return False

def validate_score(score):
    """
    Validate if a score is between 0 and 100.
    
    Args:
        score (str): The score to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        score_float = float(score)
        return 0 <= score_float <= 100
    except (ValueError, TypeError):
        return False

def calculate_age(dob):
    """
    Calculate age based on date of birth.
    
    Args:
        dob (str): Date of birth in ISO format (YYYY-MM-DD)
        
    Returns:
        int: Age in years
    """
    birth_date = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
    today = datetime.date.today()
    
    age = today.year - birth_date.year
    
    # Adjust age if birthday hasn't occurred yet this year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age

def setup_module():
    """
    Allows the user to define assessment criteria for any module.
    
    Returns:
        dict: Module configuration
    """
    print("Welcome to the Student Grading System")
    print("First, let's set up the module configuration.")
    
    module_name = input("Enter module name: ")
    
    while True:
        try:
            num_components = int(input("How many assessment components does this module have? "))
            if num_components > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    components = []
    weights = []
    
    for i in range(num_components):
        component_name = input(f"Component {i+1} name: ")
        
        while True:
            try:
                component_weight = float(input(f"Component {i+1} weight (%): "))
                if 0 <= component_weight <= 100:
                    weights.append(component_weight / 100)  # Convert percentage to decimal
                    break
                else:
                    print("Weight must be between 0 and 100.")
            except ValueError:
                print("Please enter a valid number.")
        
        components.append(component_name)
    
    # Normalize weights to sum to 1
    total_weight = sum(weights)
    if total_weight != 1:
        weights = [w / total_weight for w in weights]
    
    return {
        "module_name": module_name,
        "components": components,
        "weights": weights
    }

def advanced(filename, weights=None):
    """
    Reads student data from a file and processes it.
    
    Args:
        filename (str): The name of the file to read
        weights (list, optional): List of weights for component scores
        
    Returns:
        None
    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        # Parse student data from file
        students = []
        i = 0
        while i < len(lines):
            if i + 7 <= len(lines):  # Need 7 lines per student (ID, Name, DOB, 4 scores)
                student_id = lines[i].strip()
                name = lines[i+1].strip()
                dob = lines[i+2].strip()
                
                scores = []
                for j in range(4):
                    try:
                        scores.append(float(lines[i+3+j].strip()))
                    except ValueError:
                        scores.append(0)  # Default to 0 if score is invalid
                
                students.append({
                    "id": student_id,
                    "name": name,
                    "dob": dob,
                    "scores": scores
                })
                
                i += 7
            else:
                break
        
        # Process student data
        processed_students = []
        for student in students:
            overall_score = calculate_overall_score(student["scores"], weights)
            category = determine_category(overall_score)
            age = calculate_age(student["dob"])
            rounded_result = round_to_category(overall_score)
            
            processed_students.append({
                "uid": student["id"],
                "name": student["name"],
                "dob": student["dob"],
                "age": age,
                "raw_score": overall_score,
                "rounded_score": rounded_result[0],
                "category": rounded_result[1]
            })
        
        # Sort by UID
        processed_students.sort(key=lambda s: s["uid"])
        
        # Generate table
        table_data = []
        for student in processed_students:
            table_data.append([
                student["uid"],
                student["name"],
                student["dob"],
                student["age"],
                student["raw_score"],
                student["rounded_score"],
                student["category"]
            ])
        
        headers = ["UID", "Name", "D.o.B", "Age", "Raw Score", "Rounded Score", "Category"]
        table = tabulate(table_data, headers=headers, tablefmt="grid")
        
        # Display table
        print(table)
        
        # Write table to file
        with open("students.txt", 'w') as file:
            file.write(table)
        
        print("Results have been saved to students.txt")
        
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """
    Main function to run the student grading system.
    """
    print("Welcome to the Student Grading System")
    
    students = []
    student_count = 0
    student_ids = []
    
    while student_count < 3:
        print(f"\nStudent {student_count + 1}:")
        
        # Get student ID
        while True:
            student_id = input("Enter student ID (2-digit number) or 'end' to finish: ")
            
            if student_id.lower() == "end":
                break
                
            if not validate_student_id(student_id, student_ids):
                print("The input you entered was invalid. Please enter a 2-digit number.")
                continue
            
            student_ids.append(student_id)
            break
        
        if student_id.lower() == "end":
            break
        
        # Get student name
        name = input("Enter student name: ")
        
        # Get date of birth
        while True:
            dob = input("Enter date of birth (YYYY-MM-DD): ")
            if validate_dob(dob):
                break
            else:
                print("The input you entered was invalid. Please use YYYY-MM-DD format.")
        
        # Get component scores
        scores = []
        components = ["Coursework 1", "Coursework 2", "Coursework 3", "Final Exam"]
        
        for component in components:
            while True:
                score = input(f"Enter {component} score (0-100): ")
                if validate_score(score):
                    scores.append(float(score))
                    break
                else:
                    print("The input you entered was invalid. Please enter a number between 0 and 100.")
        
        # Calculate overall score and category
        overall_score = calculate_overall_score(scores)
        category = determine_category(overall_score)
        
        # Calculate age
        age = calculate_age(dob)
        
        # Get rounded score and category
        rounded_result = round_to_category(overall_score)
        
        # Store student data
        students.append({
            "uid": student_id,
            "name": name,
            "dob": dob,
            "age": age,
            "raw_score": overall_score,
            "rounded_score": rounded_result[0],
            "category": rounded_result[1]
        })
        
        student_count += 1
    
    if students:
        # Sort students by UID
        students.sort(key=lambda s: s["uid"])
        
        # Generate table
        table_data = []
        for student in students:
            table_data.append([
                student["uid"],
                student["name"],
                student["dob"],
                student["age"],
                f"{student['raw_score']:.4f}",
                student["rounded_score"],
                student["category"]
            ])
        
        headers = ["UID", "Name", "D.o.B", "Age", "Raw Score", "Rounded Score", "Category"]
        table = tabulate(table_data, headers=headers, tablefmt="grid")
        
        # Display table
        print("\nStudent Results:")
        print(table)
        
        # Write table to file
        with open("students.txt", 'w') as file:
            file.write(table)
        
        print("\nResults have been saved to students.txt")
    else:
        print("No student data was entered.")

if _name_ == "_main_":
    main()
