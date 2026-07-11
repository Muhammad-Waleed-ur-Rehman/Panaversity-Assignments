# Prompts Used

## Initial Prompt

I have attached an Excel result card containing assignment, quiz, midterm, final exam, participation scores, and grading rules. Write a Python script that calculates my current grade using the exact category weights, dropped-score rules, replacement rule, and bonus rule.

## Improved Prompt

Build a reusable grade calculator that:

1. Converts each earned score into a percentage.
2. Drops the lowest two assignment percentages.
3. Drops the lowest quiz percentage.
4. Applies these weights: Assignments 20%, Quizzes 15%, Midterm 1 15%, Midterm 2 15%, Final Exam 35%.
5. Replaces the lower midterm percentage with the final exam percentage only when the final exam percentage is higher.
6. Adds participation bonus points after the weighted calculation and caps the grade at 100%.
7. Shows each intermediate result so I can verify the calculation.
8. Calculates the exact final-exam score needed to reach a target overall grade of 96%.
9. Clearly states when the target is mathematically impossible.
10. Keeps all scores and policy values easy to update.

## Final Refinement Prompt

Do not claim the workbook contains real personal grades when the workbook itself labels the data as dummy data. Separate verified calculations from assumptions and explain the target-grade result honestly.
