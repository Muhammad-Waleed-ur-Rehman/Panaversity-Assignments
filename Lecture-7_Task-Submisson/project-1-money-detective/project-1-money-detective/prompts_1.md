# Prompts Used

## Initial Prompt

I have attached my bank statement in CSV format. Write a Python script that reads the transaction date, description, and amount and identifies recurring charges, possible forgotten subscriptions, and duplicate or repeated payments. Also calculate total inflows, total outflows, and net movement.

## Improved Prompt

Act as a personal “Money Detective.” Build a reusable Python script that:

1. Automatically finds the date, description, amount, category, and balance columns even when their headings vary.
2. Cleans transaction descriptions before comparing them.
3. Flags exact duplicates using the same date, amount, and cleaned description.
4. Flags possible duplicates when the amount is identical, dates are within three days, and descriptions are at least 70% similar.
5. Identifies recurring or contract-like charges using keywords such as subscription, membership, internet, electricity, mobile, and service charges.
6. Summarizes repeated merchants and spending categories.
7. Reconciles opening balance plus net transactions to closing balance.
8. Exports all findings into separate CSV files and explains that flags require human review.
9. Accepts a fresh CSV file from the command line so I can reuse it monthly.

## Final Refinement Prompt

Do not label every recurring payment as waste. Separate facts from review flags. Clearly state that a recurring candidate or possible duplicate must be checked against receipts or the banking app before action is taken. Highlight any data-quality issue, especially inconsistent currency labels.
