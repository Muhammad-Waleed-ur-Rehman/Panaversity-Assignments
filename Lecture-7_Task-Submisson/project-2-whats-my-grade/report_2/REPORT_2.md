# Project 2 Report - What's My Grade, Really?

**Student:** Muhammad Waleed-ur-Rehman  
**AI Tool:** ChatGPT

## 1. Project Title and Problem

This project calculates a student's true grade by encoding teacher-specific grading rules that ordinary grade apps may not support, including dropped scores, weighted categories, conditional exam replacement, and bonus points.

## 2. Data and Policy

The workbook supplies ten assignments, eight quizzes, two midterms, one final exam, and participation bonus points. It also supplies the exact policy. However, the workbook identifies these figures as dummy data, so this is a verified demonstration rather than a claim about an actual personal result.

## 3. AI Approach

ChatGPT was used as a technical client. The initial request described the desired outcome. Later prompts clarified the order of operations, required transparent intermediate calculations, added target-grade analysis, and required the script to identify impossible targets.

## 4. Verification

The assignment category was verified manually. After converting all assignment scores to percentages, the two lowest results, 56% and 60%, were removed. The remaining eight percentages averaged 85.875%, exactly matching the script.

## 5. Final Result

The calculated current grade is **89.725%**. The final exam score of 90% replaces the lower midterm score of 78%, because it is higher. The weighted subtotal is 87.225%, and the 2.5-point participation bonus produces the final result.

## 6. Target Grade

The script calculates that a **102.55%** final-exam score would be needed to achieve a **96%** overall grade. Therefore, the target is impossible under the supplied rules. A perfect 100% final exam would produce a maximum overall grade of **94.725%**.

## 7. What Worked

The script successfully handled all category weights, score drops, replacement logic, bonus application, grade cap, and target-grade calculation.

## 8. Challenges and Limitations

The main issue was that the workbook was presented as a result card, but its own instructions describe the data as dummy data. This was documented to preserve accuracy. The script also assumes no additional bonus or replacement rules beyond those stated.

## 9. Learning

The project showed that grading rules must be applied in the correct sequence. A visually convincing answer is not enough; one category should be independently recalculated to establish trust in the result.
