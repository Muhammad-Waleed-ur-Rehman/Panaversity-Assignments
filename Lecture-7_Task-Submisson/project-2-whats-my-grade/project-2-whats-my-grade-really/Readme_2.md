# Project 2 - What's My Grade, Really?

## Problem

Generic grade apps do not know a teacher's exact rules. This project encodes the supplied policy, including category weights, dropped scores, a final-exam replacement rule, and participation bonus points.

## Important Data Note

The attached workbook explicitly labels its scores as **dummy data**. Therefore, this project demonstrates the full calculation correctly, but the figures should not be presented as a real personal academic result until the workbook is updated with actual scores.

## Supplied Grading Policy

| Category | Weight | Rule |
|---|---:|---|
| Assignments | 20% | Drop the lowest 2 scores |
| Quizzes | 15% | Drop the lowest 1 score |
| Midterm 1 | 15% | Lower midterm may be replaced |
| Midterm 2 | 15% | Lower midterm may be replaced |
| Final Exam | 35% | Replaces lower midterm if higher |
| Participation | Up to 3 points | Added after weighting; grade capped at 100% |

## Calculated Result

- Assignment average after drops: **85.875%**
- Quiz average after drops: **85.000%**
- Lower midterm: **78%**
- Higher midterm: **82%**
- Final exam: **90%**
- Replacement triggered: **Yes**
- Weighted grade before bonus: **87.225%**
- Participation bonus: **2.5 percentage points**
- Current final grade: **89.725%**

## Manual Verification

The assignment category was verified by hand.

Assignment percentages:

90%, 75%, 92%, 80%, 60%, 83.333%, 95%, 56%, 86.667%, 85%

After dropping the two lowest scores, **56% and 60%**, the remaining eight percentages total **687%**.

`687 / 8 = 85.875%`

The script returns the same assignment average: **85.875%**.

## Target Grade Analysis

To reach an overall grade of **96%**, the final exam would need to be **102.55%** under the supplied rules. Since an ordinary exam is capped at 100%, the target is not achievable.

Even with a perfect **100% final exam**, the maximum overall grade would be **94.725%**.

## How to Run

```bash
python grade_calculator_2.py
python grade_calculator_2.py --final 95 --target 96
```

## What Worked

- All supplied grading rules were encoded.
- Dropped scores were applied before category averaging.
- The lower-midterm replacement rule worked correctly.
- The script explains when a target grade is impossible.
- Scores can be updated for later use.

## Limitations

- The workbook contains dummy data.
- Grade outcomes depend entirely on the accuracy of the supplied policy.
- Extra-credit opportunities beyond the stated participation bonus are not included.
