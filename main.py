
import pandas as pd
import numpy as np

# ==========================================
# STUDENT PERFORMANCE ANALYTICS SYSTEM
# ==========================================

SUBJECTS = [
    "Python",
    "Mathematics",
    "Computer_Fundamentals"
]

# 1. Load and validate the dataset
def load_data():
    df = pd.read_csv("students.csv")

    required_columns = [
        "Student_ID", "Name", "Department",
        "Python", "Mathematics",
        "Computer_Fundamentals", "Attendance",
        "Weekly_Study_Hours", "Assignments_Completed",
        "Lab_Performance"
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    if df.empty:
        raise ValueError("The dataset is empty.")

    if df["Student_ID"].duplicated().any():
        raise ValueError("Student IDs must be unique.")

    numeric_columns = SUBJECTS + [
        "Attendance", "Weekly_Study_Hours",
        "Assignments_Completed", "Lab_Performance"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column], errors="raise"
        )

        if df[column].isna().any():
            raise ValueError(
                f"Missing values in {column}"
            )

    if not df[SUBJECTS + ["Lab_Performance"]].apply(
        lambda column: column.between(0, 100).all()
    ).all():
        raise ValueError("Marks must be between 0 and 100.")

    if not df["Attendance"].between(0, 100).all():
        raise ValueError("Attendance must be between 0 and 100.")

    if not df["Assignments_Completed"].between(0, 10).all():
        raise ValueError(
            "Assignments completed must be between 0 and 10."
        )

    if (df["Weekly_Study_Hours"] < 0).any():
        raise ValueError("Study hours cannot be negative.")

    return df

# 2. Calculate marks and academic averages
def calculate_performance(df):
    df["Total_Marks"] = df[SUBJECTS].sum(axis=1)
    df["Average_Marks"] = df[SUBJECTS].mean(axis=1).round(2)

    return df

# 3. Assign grades
def assign_grade(average):
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"

# 4. Assign pass/fail status
def assign_results(df):
    # Passing requires at least 40 in every subject
    passed = (df[SUBJECTS] >= 40).all(axis=1)

    df["Result"] = np.where(passed, "Pass", "Fail")
    df["Grade"] = df["Average_Marks"].apply(assign_grade)

    return df

# 5. Analyze the overall class
def class_analysis(df):
    print("\n" + "=" * 55)
    print("             CLASS PERFORMANCE SUMMARY")
    print("=" * 55)

    print("Total students:", len(df))
    print("Class average:", round(df["Average_Marks"].mean(), 2))
    print("Highest student average:", df["Average_Marks"].max())
    print("Lowest student average:", df["Average_Marks"].min())

    print("Students passed:", (df["Result"] == "Pass").sum())
    print("Students failed:", (df["Result"] == "Fail").sum())

    print("\nSUBJECT-WISE ANALYSIS")

    for subject in SUBJECTS:
        print(
            f"{subject}: "
            f"Average = {df[subject].mean():.2f}, "
            f"Highest = {df[subject].max()}, "
            f"Lowest = {df[subject].min()}"
        )

# 6. Find top performers
def show_top_performers(df):
    print("\n" + "=" * 55)
    print("                  TOP 3 STUDENTS")
    print("=" * 55)

    top_students = df.sort_values(
        by="Average_Marks",
        ascending=False
    ).head(3)

    print(
        top_students[
            ["Student_ID", "Name", "Average_Marks", "Grade"]
        ].to_string(index=False)
    )

# 7. Explore study habits and practical skills
def analyze_learning_patterns(df):
    print("\n" + "=" * 55)
    print("              LEARNING PATTERN ANALYSIS")
    print("=" * 55)

    print(
        "Average weekly study hours:",
        round(df["Weekly_Study_Hours"].mean(), 2)
    )

    print(
        "Average attendance:",
        round(df["Attendance"].mean(), 2), "%"
    )

    print(
        "Average assignments completed:",
        round(df["Assignments_Completed"].mean(), 2),
        "out of 10"
    )

    print(
        "Average lab performance:",
        round(df["Lab_Performance"].mean(), 2)
    )

    # Correlation describes association, not causation
    correlation = np.corrcoef(
        df["Weekly_Study_Hours"],
        df["Average_Marks"]
    )[0, 1]

    print(
        "Study-hours and marks correlation:",
        round(correlation, 2)
    )

    if correlation > 0.3:
        print("Observation: Higher study hours tend to be associated with higher marks.")
    elif correlation < -0.3:
        print("Observation: Higher study hours tend to be associated with lower marks in this dataset.")
    else:
        print("Observation: The relationship between study hours and marks is weak.")

# 8. Compare theory and practical performance
def practical_analysis(df):
    df["Practical_Gap"] = (
        df["Lab_Performance"] - df["Average_Marks"]
    ).round(2)

    print("\n" + "=" * 55)
    print("           THEORY VS PRACTICAL PERFORMANCE")
    print("=" * 55)

    print(
        df[
            ["Name", "Average_Marks", "Lab_Performance", "Practical_Gap"]
        ].sort_values(
            by="Practical_Gap", ascending=False
        ).to_string(index=False)
    )

# 9. Main program
def main():
    try:
        df = load_data()
        df = calculate_performance(df)
        df = assign_results(df)

        print("\nSTUDENT PERFORMANCE ANALYTICS SYSTEM")
        print("-" * 55)

        print(df.to_string(index=False))

        class_analysis(df)
        show_top_performers(df)
        analyze_learning_patterns(df)
        practical_analysis(df)

        # Export the complete analysis
        df.to_csv("student_analysis_results.csv", index=False)

        print("\nAnalysis saved to student_analysis_results.csv")
        print("Project completed successfully!")

    except FileNotFoundError:
        print("Error: students.csv was not found.")
        print("Keep students.csv in the same folder as main.py.")

    except (ValueError, KeyError) as error:
        print("Data error:", error)

if __name__ == "__main__":
    main()