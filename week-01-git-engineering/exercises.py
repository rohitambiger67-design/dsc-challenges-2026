
"""Week 0: Python Fundamentals Bootcamp — Beginner Practice Tasks."""

import csv
import json
from typing import Dict, List, Tuple, Any


# TASK 1a: Attendance Status

def evaluate_attendance_status(attended: int, total: int) -> str:
    """Return 'ELIGIBLE' (>=75%), 'WARNING' (65% to <75%), or 'SHORTAGE' (<65%).

    If total <= 0, return 'NO_SESSIONS'.
    """
    if total <= 0:
        return "NO_SESSIONS"

    percentage = (attended / total) * 100

    if percentage >= 75:
        return "ELIGIBLE"
    elif percentage >= 65:
        return "WARNING"
    else:
        return "SHORTAGE"


# TASK 1b: Safe Float Conversion

def safe_parse_float(raw_value: Any, default: float = 0.0) -> float:
    """Convert raw_value to float safely using try/except. Return default on failure."""

    try:
        return float(raw_value)
    except (ValueError, TypeError):
        return default


# TASK 2: Collections and Comprehensions

def analyze_pod_scores(records: List[Tuple[str, str, float]]) -> Dict[str, Any]:
    """Analyze (usn, pod_name, score) tuples using sets, dicts, and comprehensions.

    Returns a dictionary with keys:
      - 'unique_student_count': int (number of unique USNs via set)
      - 'high_scorers': List[str] (USNs with score >= 80 using a list comprehension)
      - 'pod_averages': Dict[str, float] (average score per pod rounded to 2 decimals)
    """

    # Store unique USNs
    unique_usns = set()

    # Store scores grouped by pod
    pod_scores = {}

    for usn, pod_name, score in records:
        unique_usns.add(usn)

        if pod_name not in pod_scores:
            pod_scores[pod_name] = []

        pod_scores[pod_name].append(score)

    # Find students scoring 80 or above
    high_scorers = [
        usn for usn, pod_name, score in records
        if score >= 80
    ]

    # Calculate average score for each pod
    pod_averages = {
        pod: round(sum(scores) / len(scores), 2)
        for pod, scores in pod_scores.items()
    }

    return {
        "unique_student_count": len(unique_usns),
        "high_scorers": high_scorers,
        "pod_averages": pod_averages
    }


# TASK 3: CSV to JSON File I/O

def summarize_csv_to_json(csv_path: str, json_path: str) -> Dict[str, Any]:
    """Read cohort CSV using built-in csv module and export summary JSON.

    Summary dictionary must contain:
      - 'total_students': int
      - 'branches': List[str] (sorted unique branch codes)
      - 'average_score': float (rounded to 2 decimals)
    """

    # Read CSV file
    with open(csv_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        records = list(reader)

    # Count students
    total_students = len(records)

    # Find unique branches
    branches = sorted({
        record["branch"] for record in records
    })

    # Extract scores
    scores = [
        float(record["score"]) for record in records
    ]

    # Calculate average
    if total_students > 0:
        average_score = round(sum(scores) / total_students, 2)
    else:
        average_score = 0.0

    # Create summary dictionary
    summary = {
        "total_students": total_students,
        "branches": branches,
        "average_score": average_score
    }

    # Write summary into JSON file
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    return summary


# TASK 4: Object-Oriented Programming

class StudentRecord:
    """Tracks weekly evaluation scores for a single DSC recruit."""

    def __init__(self, usn: str, name: str):
        """Initialize record with uppercase USN, name, and empty scores list."""

        self.usn = usn.strip().upper()
        self.name = name
        self.scores = []

    def add_score(self, score: float) -> None:
        """Append a score (must be between 0 and 100; raise ValueError otherwise)."""

        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100")

        self.scores.append(float(score))

    def average(self) -> float:
        """Return average score rounded to 2 decimals, or 0.0 if no scores exist."""

        if len(self.scores) == 0:
            return 0.0

        return round(sum(self.scores) / len(self.scores), 2)

    def is_passing(self, threshold: float = 50.0) -> bool:
        """Return True if average() >= threshold, else False."""

        return self.average() >= threshold

