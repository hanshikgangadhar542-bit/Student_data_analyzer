import csv
import tkinter as tk
from tkinter import filedialog, messagebox


# ----------------- PROCESSING FUNCTIONS -----------------

def preprocess_csv(file_name):
    cleaned_data = []
    total_marks = 0
    count = 0

    with open(file_name, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Name'] == '' or row['Grade'] == '' or row['Marks'] == '':
                continue

           
            row['Marks'] = int(row['Marks'])

            cleaned_data.append(row)
            total_marks += row['Marks']
            count += 1

    avg = total_marks / count if count > 0 else 0
    return cleaned_data, avg


def count_students_per_grade(cleaned_data):
    grade_count = {}
    for row in cleaned_data:
        grade = row['Grade']
        grade_count[grade] = grade_count.get(grade, 0) + 1
    return grade_count


def top_three_scorers(cleaned_data):
    return sorted(cleaned_data, key=lambda x: x['Marks'], reverse=True)[:3]


# ----------------- GUI FUNCTIONS -----------------

def choose_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_path:
        return

    try:
        cleaned_data, avg = preprocess_csv(file_path)
        grade_count = count_students_per_grade(cleaned_data)
        top3 = top_three_scorers(cleaned_data)

        output = (
            f"Average Marks: {avg:.2f}\n\n"
            "Students Per Grade:\n"
        )

        for grade, count in grade_count.items():
            output += f"  Grade {grade}: {count}\n"

        output += "\nTop 3 Scorers:\n"
        for s in top3:
            output += f"  {s['Name']} - {s['Marks']}\n"

        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, output)

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")


# ----------------- BUILD THE GUI -----------------

window = tk.Tk()
window.title("Student CSV Processor")
window.geometry("500x500")

title = tk.Label(window, text="Student Data Analyzer", font=("Arial", 16))
title.pack(pady=10)

btn = tk.Button(window, text="Select CSV File", command=choose_file, font=("Arial", 12))
btn.pack(pady=10)

result_box = tk.Text(window, height=20, width=60, font=("Arial", 10))
result_box.pack(pady=10)

window.mainloop()
