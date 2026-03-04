import os
import json
import csv
import argparse
import sys

# Add the olm_ocr_project to path so we can import ocr_processor
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "olm_ocr_project"))
import ocr_processor

def calculate_averages(data):
    """
    Maps the first 7 handwritten survey questions (Q1-Q7) directly to 
    the 7 standardized report categories. Remaining questions (Q8-Q14) 
    are ignored as per user requirement.
    
    Mapping:
    1. Preparation & Organization (Q1)
    2. Subject knowledge & Expertise (Q2)
    3. Explanation & Empathy (Q3)
    4. Discipline & Punctuality (Q4)
    5. Regularity & Timeliness (Q5)
    6. Encouragement to Learning (Q6)
    7. Teacher availability (Q7)
    """
    def parse_score(q_key):
        val = str(data.get(q_key, "0")).strip().split()[0] # Take first char/word
        try:
            return float(val)
        except ValueError:
            return 0.0

    # Only take the first 7 scores
    cat_avgs = [parse_score(f"Q{i}") for i in range(1, 8)]
    
    total_score = sum(cat_avgs)
    percentage = (total_score / 35.0) * 100
    return cat_avgs, total_score, percentage

def update_csv(csv_file, dept, teacher, cat_avgs, total_score, percentage):
    file_exists = os.path.isfile(csv_file) and os.path.getsize(csv_file) > 0
    headers = [
        "Name of the Teacher",
        "Preparation & Organization for Class (5)",
        "Subject knowledge & Expertise (5)",
        "Explanation & Empathy to student (5)",
        "Discipline & Punctuality (5)",
        "Regularity & Timeliness (5)",
        "Encouragement to Participative Learning (5)",
        "Teacher availability beyond classroom (5)",
        "Total (35)",
        "Percentage of score"
    ]
    
    row = [teacher] + [round(a, 3) for a in cat_avgs] + [round(total_score, 2), f"{percentage:.2f}%"]

    with open(csv_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Students' Satisfaction Survey Report for the 2025 Odd (Autumn) Semester"])
            writer.writerow([f"Department of {dept}"])
            writer.writerow(["Feedback Regarding Teacher"])
            writer.writerow([])
            writer.writerow(headers)
        writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description="Automated Survey Processing Pipeline")
    parser.add_argument("--input_dir", type=str, default="../input", help="Directory with survey images")
    parser.add_argument("--output_csv", type=str, default="survey_reports.csv", help="Output CSV file")
    parser.add_argument("--mock", action="store_true", help="Run in mock mode")
    args = parser.parse_args()

    input_dir = os.path.abspath(args.input_dir)
    output_csv = os.path.abspath(args.output_csv)

    print(f"Starting pipeline processing for input: {input_dir}")

    # For this implementation, we assume images are directly in input_dir
    # In a more complex setup, they might be in subfolders per teacher.
    # The ocr_processor handles per-folder logic.

    if args.mock:
        print("Running in MOCK mode...")
        # Simulating one teacher/department extraction
        mock_data = {
            "Department": "Nursing",
            "Semester": "7th",
            "Year": "2025",
            "CourseCode": "NURS101",
            "CourseName": "B.Sc Nursing",
            "TaughtBy": "Dr. Rumi Sen",
            "FullPart": "Full",
            "Q1": "5", "Q2": "5", "Q3": "5", "Q4": "5", "Q5": "5",
            "Q6": "5", "Q7": "5", "Q8": "5", "Q9": "5", "Q10": "5",
            "Q11": "5", "Q12": "5", "Q13": "5", "Q14": "5",
            "Q15": "Excellent teacher."
        }
        extracted_data_list = [mock_data]
    else:
        # Actual OCR logic would go here, calling ocr_processor functions
        # This requires model loading which we might skip for the demo/verification
        print("Model-based OCR not fully active in this script environment (requires GPU/Model).")
        return

    for data in extracted_data_list:
        teacher = data.get("TaughtBy", "Unknown")
        dept = data.get("Department", "General")
        
        cat_avgs, total_score, percentage = calculate_averages(data)
        
        print(f"Updating report for: {teacher} ({dept})")
        update_csv(output_csv, dept, teacher, cat_avgs, total_score, percentage)

    print(f"Pipeline complete. Results in {output_csv}")

if __name__ == "__main__":
    main()
