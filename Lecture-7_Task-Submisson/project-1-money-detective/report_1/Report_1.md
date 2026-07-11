# AI Projects Report

**Student:** Muhammad Waleed-ur-Rehman  
**Project covered in this report:** Project 1 — Money Detective

## 1. Project Title and Problem Solved

**Money Detective** examines past bank transactions instead of asking the user to begin a new budget. It searches for recurring commitments, possible forgotten subscriptions, duplicate or repeated payments, and concentrated spending patterns. The goal is to produce a small number of findings that the user can verify and act upon.

## 2. AI Tool Used

I used ChatGPT to convert my business requirement into a reusable Python program. I treated the AI as a technical service provider: I described the required outcome, asked for transparent detection rules, tested the output, and then requested improvements.

## 3. Prompts and Iterations

The initial prompt asked for recurring-charge and duplicate-payment detection. The improved prompt added automatic column detection, text cleaning, exact and fuzzy duplicate rules, recurring-charge keywords, merchant summaries, balance reconciliation, CSV exports, and human-review warnings. The final refinement required the script to distinguish proven totals from review flags and to report currency-label inconsistencies.

The complete prompt history is saved in `project-1-money-detective/prompts_1.md`.

## 4. Verification

I verified more than two figures:

| Check | Manual / Known Figure | Script Figure | Difference |
|---|---:|---:|---:|
| Total outflows | 3,442.85 | 3,442.85 | 0.00 |
| Opening-to-closing movement | 2,977.15 | 2,977.15 | 0.00 |
| Total inflows | 6,420.00 | 6,420.00 | 0.00 |
| Closing balance reconciliation | 11,477.15 | 11,477.15 | 0.00 |

The exact reconciliation increased confidence that the script read the signs and amounts correctly.

## 5. What Worked

The Python program successfully read the CSV, calculated inflows and outflows, reconciled the balance, identified six contract-like charges, summarized repeated merchants, and exported structured result files. It found no exact or high-confidence duplicate charge, which is itself a valid result.

## 6. What Did Not Work and Problems Faced

Only one month of data was available, so statistical recurrence could not be confirmed across multiple months. The script therefore uses keywords to create a review list rather than claiming every item is a subscription. Transaction descriptions are also inconsistent, making duplicate matching imperfect. Cash withdrawals cannot be traced to final spending categories. Finally, the source file labels transaction amounts as AED but balances as PKR; the numerical movement reconciles, yet the currency labels require confirmation.

## 7. Final Result and Action Taken

The script identified six contract-like charges totaling **969.00**. The most practical review items are Netflix (**35.00**), Fitness First (**250.00**), and bank service charges (**25.00**). Together, these amount to **310.00 per month** and potentially **3,720.00 per year**. I can now confirm whether I still use these services and whether the bank fee can be reduced or avoided.

No duplicate payment was detected. Three Careem rides totaling **145.00** were identified as a repeated spending pattern.

## 8. Learning

The main lesson was that AI-generated analysis should not be trusted merely because the output looks professional. The totals must be tied back to known balances and manually checked values. Once those checks pass, AI becomes useful for converting raw transaction history into a focused and repeatable monthly review.
