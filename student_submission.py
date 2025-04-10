import datetime
from tabulate import tabulate

# Grade boundaries for categories
grade_boundaries = [85, 75, 68, 60, 52, 40, 0]
categories = ["Upper-First", "First", "2:1", "2:2", "Third", "Fail"]

# ----- Function Definitions -----

def validate_score(prompt):
    while True:
        try:
            score = float(input(prompt))
            if 0 <= score <= 100:
                return score
            else:
                print("The input you entered was invalid. Score must be between 0 and 100.")
        except ValueError:
            print("The input you entered was invalid. Please enter a number.")

def validate_dob(prompt):
    while True:
        try:
            dob = input(prompt)
            datetime.datetime.strptime(dob, "%Y-%m-%d")
            return dob
        except ValueError:
            print("The input you entered was invalid. Please enter date in YYYY-MM-DD format.")

def validate_uid(prompt):
    while True:
        uid = input(prompt)
        if uid.lower() == 'end':
            return 'end'
        if uid.isdigit() and len(uid) == 2:
            return uid
        else:
            print("The input you entered was invalid. Please enter a 2-digit number.")

def calculate_age(dob):
    birth_date = datetime.datetime.strptime(dob, "%Y-%m-%d")
    today = datetime.datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def calculate_overall_score(scores, weights):
    weighted_scores = [score * (w / 100) for score, w in zip(scores, weights)]
    return round(sum(weighted_scores), 4)

def determine_category(score):
    for i, boundary in enumerate(grade_boundaries):
        if score >= boundary:
            return categories[i]
    return "Fail"

def round_to_category(score):
    all_boundaries = grade_boundaries[:-1]  # exclude 0
    for i in range(len(all_boundaries) - 1):
        lower = all_boundaries[i+1]
        upper = all_boundaries[i]
        mid = (lower + upper) / 2
        if lower < score < upper:
            if score >= mid:
                return (upper, determine_category(upper))
            else:
                return (lower, determine_category(lower))
    if score >= all_boundaries[0]:
        return (all_boundaries[0], determine_category(all_boundaries[0]))
    return (0, "Fail")

def setup_module():
    print("Welcome to the Student Grading System\nFirst, let's set up the module configuration.")
    module_name = input("Enter module name: ")
    while True:
        try:
            num_components = int(input("How many assessment components does this module have? "))
            break
        except ValueError:
            print("The input you entered was invalid. Please enter a number.")
    components = []
    weights = []
    total_weight = 0
    for i in range(num_components):
        name = input(f"Component {i+1} name: ")
        while True:
            try:
                weight = float(input(f"Component {i+1} weight (%): "))
                if 0 <= weight <= 100:
                    components.append(name)
                    weights.append(weight)
                    total_weight += weight
                    break
                else:
                    print("The input you entered was invalid. Weight must be between 0 and 100.")
            except ValueError:
                print("The input you entered was invalid. Please enter a number.")
    if total_weight != 100:
        print("Weights do not sum up to 100%. Restarting module setup.")
        return setup_module()
    return module_name, components, weights

def main():
    module_name, components, weights = setup_module()
    students = []
    while len(students) < 3:
        uid = validate_uid("Enter student ID (2-digit) or 'end' to finish: ")
        if uid == 'end':
            break
        name = input("Enter name: ")
        dob = validate_dob("Enter date of birth (YYYY-MM-DD): ")
        age = calculate_age(dob)
        scores = [validate_score(f"Enter score for {comp}: ") for comp in components]
        raw_score = calculate_overall_score(scores, weights)
        rounded_score, category = round_to_category(raw_score)

        students.append({
            "UID": uid,
            "Name": name,
            "DOB": dob,
            "Age": age,
            "Raw Score": raw_score,
            "Rounded Score": rounded_score,
            "Category": category
        })

    students.sort(key=lambda x: x["UID"])
    headers = ["UID", "Name", "D.O.B", "Age", "Raw Score", "Rounded Score", "Category"]
    table = [[s["UID"], s["Name"], s["DOB"], s["Age"], s["Raw Score"], s["Rounded Score"], s["Category"]] for s in students]
    print("\nResults:")
    print(tabulate(table, headers=headers, tablefmt="github"))

    with open("students.txt", "w") as f:
        f.write(tabulate(table, headers=headers, tablefmt="github"))

def advanced(filename, weights):
    with open(filename, "r") as f:
        lines = f.readlines()
    students = []
    for line in lines:
        uid, name, dob = line.strip().split(",")
        age = calculate_age(dob)
        print(f"Enter scores for {name}:")
        scores = [validate_score(f"Component {i+1}: ") for i in range(len(weights))]
        raw_score = calculate_overall_score(scores, weights)
        rounded_score, category = round_to_category(raw_score)

        students.append({
            "UID": uid,
            "Name": name,
            "DOB": dob,
            "Age": age,
            "Raw Score": raw_score,
            "Rounded Score": rounded_score,
            "Category": category
        })

    students.sort(key=lambda x: x["UID"])
    headers = ["UID", "Name", "D.O.B", "Age", "Raw Score", "Rounded Score", "Category"]
    table = [[s["UID"], s["Name"], s["DOB"], s["Age"], s["Raw Score"], s["Rounded Score"], s["Category"]] for s in students]
    print("\nResults:")
    print(tabulate(table, headers=headers, tablefmt="github"))

    with open("students.txt", "w") as f:
        f.write(tabulate(table, headers=headers, tablefmt="github"))

# Run main if executed directly
if __name__ == "__main__":
    main()
