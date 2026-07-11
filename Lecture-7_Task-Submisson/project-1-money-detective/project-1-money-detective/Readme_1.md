# Project 1 — Money Detective

## Problem

Budgeting apps usually start tracking from today. This project looks backward at real transaction history to find spending patterns, recurring commitments, forgotten subscriptions, and possible duplicate charges.

## AI Tool Used

ChatGPT was used as the “technical client” to translate the problem into a reusable Python script, improve the detection rules, explain the logic, and document the result.

## Dataset

`bank_statement_july_2026_1.csv` contains 32 rows covering July 2026. The script analyzes transaction dates, descriptions, amounts, categories, and balances.

> Data-quality note: the transaction amount heading says **AED**, while the balance heading says **PKR**. The figures still reconcile numerically, but the currency labels should be confirmed before using the report for financial decisions.

## How to Run

```bash
pip install -r requirements.txt
python money_detective_1.py bank_statement_july_2026_1.csv --output-dir results_1
```

## Verification Against Known Figures

Two independent checks were performed:

1. **Outflows:** Hand-adding all negative transactions gives **3,442.85**. The script returns **3,442.85**.
2. **Balance movement:** Closing balance **11,477.15** minus opening balance **8,500.00** equals **2,977.15**. The script calculates net transaction movement of **2,977.15**, with a reconciliation difference of **0.00**.

A third cross-check also passed: inflows of **6,420.00** less outflows of **3,442.85** equals the same net movement of **2,977.15**.

## Concrete Findings

The script found **six contract-like or recurring-review charges totaling 969.00**:

- DEWA electricity bill — 310.00
- Etisalat mobile top-up — 50.00
- du Home Fibre — 299.00
- Fitness First membership — 250.00
- Netflix subscription — 35.00
- Bank service charges — 25.00

No exact duplicate charge and no high-confidence possible duplicate pair were found.

The actionable result is to review the **Netflix subscription, gym membership, and bank service fee**. Together they cost **310.00 per month**, or **3,720.00 per year** if they continue at the same rate. This is not proof that they are unnecessary; it is a focused cancellation or renegotiation checklist.

The statement also shows repeated Careem use: three rides totaling **145.00**. This is a spending pattern rather than a billing error.

## What Worked

- The statement reconciled exactly.
- The script separated confirmed totals from items requiring human review.
- The command-line design makes it reusable on future monthly CSV files.
- Results are exported to CSV for audit trail and review.

## What Did Not Work / Limitations

- One month of data cannot prove a charge recurs monthly. Keyword-based charges are therefore called “recurring candidates.”
- Merchant descriptions can vary, so fuzzy matching may miss duplicates or produce false positives.
- ATM cash withdrawals cannot be categorized further without receipts.
- The inconsistent AED/PKR headings need confirmation from the source statement.

## What I Learned

AI can draft the code, but trust comes from reconciliation and manual checks. The useful output is not merely a list of transactions; it is a review queue supported by transparent rules and verified totals.
