# Project 3 - The Books Don't Match

## Problem

Two records should agree: a hand-counted roster total and a messy digital payment export. The raw bank total alone is misleading because it includes a duplicate transfer and an unidentified payment.

## AI Tool Used

ChatGPT was used to translate the collector's interpretation rules into a reusable Python reconciliation script, design verification controls, explain the logic, and prepare the documentation.

## Ground Truth

- 18 confirmed contributors
- PKR 2,500 per person
- Expected total: **PKR 45,000**

## Raw Digital Record

The digital payment export totals **PKR 46,500**, which is PKR 1,500 above the expected amount. However, reconciliation shows that not all of this money can be credited to roster dues.

## Interpretation Rules Applied

- Unique nicknames, initials, and short forms are mapped to roster names.
- Umer's PKR 5,000 “self+bilal” payment is split between Umer Farooq and Bilal Ahmed.
- Mrs Osman Javed's payment is credited to Osman Javed.
- Hassan Sheikh's second same-day PKR 2,500 transfer is treated as a duplicate.
- Mahnoor's PKR 1,500 payment is treated as partial.
- The unregistered PKR 2,500 transfer remains unidentified.
- Kamran's ambiguous memo is accepted because his identity and amount match.

## Reconciliation Result

| Measure | Amount |
|---|---:|
| Expected roster total | PKR 45,000 |
| Raw digital total | PKR 46,500 |
| Valid amount credited to roster | PKR 41,500 |
| Duplicate transfer | PKR 2,500 |
| Unidentified transfer | PKR 2,500 |
| Outstanding roster dues | PKR 3,500 |
| Control difference | PKR 0 |

## People Requiring Follow-Up

- **Mahnoor Iqbal:** paid PKR 1,500; collect PKR 1,000.
- **Faisal Mehmood:** no matching payment; collect PKR 2,500.
- **Hassan Sheikh:** refund or credit the duplicate PKR 2,500.
- **Unregistered sender:** identify the sender before allocating PKR 2,500.

## Manual Verification

The raw total was verified independently:

- 15 ordinary full-share transfers = PKR 37,500
- Umer's combined transfer = PKR 5,000
- Mahnoor's partial payment = PKR 1,500
- Unregistered transfer = PKR 2,500

Total: **37,500 + 5,000 + 1,500 + 2,500 = PKR 46,500**

The script also proves:

**PKR 41,500 credited + PKR 2,500 duplicate + PKR 2,500 unidentified = PKR 46,500**

## How to Run

```bash
pip install -r requirements_3.txt
python reconciliation_3.py Farewell_Gift_Reconciliation_Example_3.xlsx --output-dir results_3
```

## What Worked

- Messy names were matched using documented personal rules.
- Combined, spouse, partial, duplicate, and unidentified transactions were handled separately.
- The raw payment total reconciled with a zero control difference.
- The script names the people and exact amounts requiring action.

## Limitations

- Name mappings are based on personal knowledge and must be updated for another group.
- An unidentified transfer cannot be allocated without external confirmation.
- The dataset is explicitly described in the workbook as fictional and illustrative.
