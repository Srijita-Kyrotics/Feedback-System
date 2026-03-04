import csv
import os

def get_float_input(prompt, min_val=0, max_val=5):
    while True:
        try:
            val = float(input(prompt))
            if min_val <= val <= max_val:
                return val
            else:
                print(f"Please enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def main():
    print("=== Student Satisfaction Survey System (CLI) ===")
    
    dept = input("Enter Department: ").strip()
    teacher = input("Enter Name of the Teacher: ").strip()
    
    while True:
        try:
            num_students = int(input("Enter number of students: "))
            if num_students > 0:
                break
            print("Number of students must be at least 1.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    categories = [
        "Preparation & Organization for Class",
        "Subject Knowledge & Expertise",
        "Explanation & Empathy to student",
        "Discipline & Punctuality",
        "Regularity & Timeliness",
        "Encouragement to Participative Learning",
        "Teacher availability beyond classroom"
    ]

    category_averages = []

    for i, cat in enumerate(categories, 1):
        print(f"\nCategory {i}: {cat}")
        scores = []
        # Support space-separated input for convenience
        while len(scores) < num_students:
            remaining = num_students - len(scores)
            prompt = f"Enter scores for {remaining} more student(s) (space-separated, 0-5): "
            line_input = input(prompt).split()
            for s in line_input:
                try:
                    val = float(s)
                    if 0 <= val <= 5:
                        scores.append(val)
                    else:
                        print(f"Skipping '{s}': Must be between 0 and 5.")
                except ValueError:
                    print(f"Skipping '{s}': Not a number.")
            
            if len(scores) > num_students:
                print(f"Warning: You entered {len(scores)} scores, but only {num_students} were expected. Truncating to {num_students}.")
                scores = scores[:num_students]

        avg = sum(scores) / num_students
        category_averages.append(avg)
        print(f"-> Average for Category {i}: {avg:.3f}")

    total_score = sum(category_averages)
    percentage = (total_score / 35) * 100

    print("\n" + "="*40)
    print(f"Results for {teacher} ({dept})")
    print(f"Total Score: {total_score:.2f} / 35.00")
    print(f"Percentage: {percentage:.2f}%")
    print("="*40)

    # Prepare CSV data
    csv_file = "survey_reports.csv"
    file_exists = os.path.isfile(csv_file)
    
    headers = ["Department", "Teacher", "Num_Students"] + [f"Cat{i}_Avg" for i in range(1, 8)] + ["Total", "Percentage"]
    row = [dept, teacher, num_students] + [round(a, 3) for a in category_averages] + [round(total_score, 2), round(percentage, 2)]

    with open(csv_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow(row)

    print(f"\nReport appended to {os.path.abspath(csv_file)}")

if __name__ == "__main__":
    main()
