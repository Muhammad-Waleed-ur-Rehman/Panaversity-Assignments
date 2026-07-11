# Project 3 Report - The Books Don't Match

**Student:** Muhammad Waleed-ur-Rehman  
**AI Tool:** ChatGPT

## Project Title and Problem

The Books Don't Match reconciles a known, hand-counted farewell-gift total against a messy digital payment export. It solves the problem of misleading bank totals by distinguishing valid roster payments from duplicates, partial payments, combined transfers, and unidentified funds.

## Expected Total

The ground-truth roster contains 18 confirmed contributors at PKR 2,500 each, giving an expected total of PKR 45,000.

## AI and Prompt Process

The initial prompt asked AI to find the gap and identify unmatched amounts and people. Improved prompts specified the name-matching rules, combined-payment split, spouse payment, duplicate treatment, partial-payment logic, unidentified-transfer rule, and a zero-difference control.

## Verification

The raw payment total was independently recalculated as PKR 46,500. The script reconciled this total into PKR 41,500 validly credited to roster dues, PKR 2,500 duplicate money, and PKR 2,500 unidentified money. The control difference was zero.

## Findings and Actions

Mahnoor Iqbal still owes PKR 1,000. Faisal Mehmood has no matched payment and owes PKR 2,500. Hassan Sheikh's second PKR 2,500 transfer should be refunded or credited. The PKR 2,500 unregistered transfer requires identification.

## What Worked

The script successfully handled inconsistent names, initials, a nickname, a spouse account, a combined payment, a duplicate, a partial payment, an ambiguous memo, and an unknown sender.

## What Did Not Work and Challenges

The unidentified transfer could not be allocated automatically because doing so would violate the collector's rule. This is a deliberate limitation, not a script failure. The workbook is also labelled as a fictional illustrative example.

## Final Result and Learning

The raw total was PKR 1,500 higher than the target, yet PKR 3,500 was still outstanding from named roster members. This shows why reconciliation must follow identities and business rules rather than relying only on the total amount received.
