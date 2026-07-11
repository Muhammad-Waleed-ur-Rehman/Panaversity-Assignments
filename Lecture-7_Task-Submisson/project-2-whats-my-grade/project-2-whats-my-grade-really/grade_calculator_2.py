#!/usr/bin/env python3
"""
What's My Grade, Really?

Calculates the current grade using the supplied policy:
- Assignments: 20%, drop lowest 2
- Quizzes: 15%, drop lowest 1
- Midterm 1: 15%
- Midterm 2: 15%
- Final exam: 35%
- Final replaces the lower midterm when higher
- Participation bonus added as percentage points, capped at 100%

The default values below are taken from the attached workbook, which labels them as dummy data.
Replace them with real scores before using the result as a personal academic grade.
"""

from __future__ import annotations
import argparse

ASSIGNMENTS = [(18,20),(15,20),(23,25),(20,25),(12,20),
               (25,30),(19,20),(14,25),(26,30),(17,20)]
QUIZZES = [(9,10),(7,10),(8,10),(10,10),(6,10),(8.5,10),(7.5,10),(9.5,10)]
MIDTERM_1 = 78.0
MIDTERM_2 = 82.0
FINAL_EXAM = 90.0
PARTICIPATION_BONUS = 2.5
TARGET_GRADE = 96.0

WEIGHTS = {
    "assignments": 0.20,
    "quizzes": 0.15,
    "midterm_1": 0.15,
    "midterm_2": 0.15,
    "final_exam": 0.35,
}


def average_after_drops(scores, drop_count):
    percentages = [earned / maximum * 100 for earned, maximum in scores]
    kept = sorted(percentages)[drop_count:]
    return sum(kept) / len(kept), sorted(percentages)[:drop_count], kept


def calculate_grade(final_exam):
    assignment_avg, dropped_assignments, _ = average_after_drops(ASSIGNMENTS, 2)
    quiz_avg, dropped_quizzes, _ = average_after_drops(QUIZZES, 1)

    lower_midterm = min(MIDTERM_1, MIDTERM_2)
    higher_midterm = max(MIDTERM_1, MIDTERM_2)
    adjusted_lower = final_exam if final_exam > lower_midterm else lower_midterm

    weighted = (
        assignment_avg * WEIGHTS["assignments"]
        + quiz_avg * WEIGHTS["quizzes"]
        + adjusted_lower * WEIGHTS["midterm_1"]
        + higher_midterm * WEIGHTS["midterm_2"]
        + final_exam * WEIGHTS["final_exam"]
    )
    final_grade = min(weighted + PARTICIPATION_BONUS, 100.0)
    return {
        "assignment_avg": assignment_avg,
        "quiz_avg": quiz_avg,
        "dropped_assignments": dropped_assignments,
        "dropped_quizzes": dropped_quizzes,
        "adjusted_lower_midterm": adjusted_lower,
        "weighted_before_bonus": weighted,
        "final_grade": final_grade,
    }


def score_needed_for_target(target):
    # Search the exact score needed while respecting the replacement rule.
    low, high = 0.0, 200.0
    for _ in range(100):
        mid = (low + high) / 2
        if calculate_grade(mid)["final_grade"] >= target:
            high = mid
        else:
            low = mid
    return high


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--final", type=float, default=FINAL_EXAM)
    parser.add_argument("--target", type=float, default=TARGET_GRADE)
    args = parser.parse_args()

    result = calculate_grade(args.final)
    needed = score_needed_for_target(args.target)

    print("WHAT'S MY GRADE, REALLY?")
    print("=" * 28)
    print(f"Assignment average after dropping 2: {result['assignment_avg']:.3f}%")
    print(f"Quiz average after dropping 1:       {result['quiz_avg']:.3f}%")
    print(f"Dropped assignment percentages:     {result['dropped_assignments']}")
    print(f"Dropped quiz percentages:           {result['dropped_quizzes']}")
    print(f"Adjusted lower midterm used:         {result['adjusted_lower_midterm']:.3f}%")
    print(f"Weighted grade before bonus:         {result['weighted_before_bonus']:.3f}%")
    print(f"Participation bonus:                 {PARTICIPATION_BONUS:.3f} points")
    print(f"Current final grade:                 {result['final_grade']:.3f}%")
    print()
    print(f"Final-exam score needed for {args.target:.2f}%: {needed:.3f}%")
    if needed > 100:
        maximum = calculate_grade(100)["final_grade"]
        print(f"Target is not achievable under the supplied rules.")
        print(f"Maximum possible grade with 100% on final: {maximum:.3f}%")

if __name__ == "__main__":
    main()
