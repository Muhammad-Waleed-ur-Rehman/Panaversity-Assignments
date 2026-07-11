# Prompts Used

## Initial Prompt

I have a hand-counted expected total and an unedited digital payment record in an Excel workbook. Write a Python script that compares the two records, applies my personal interpretation rules, calculates the gap, and identifies the people and amounts requiring follow-up.

## Improved Prompt

Act as a reconciliation analyst. Read the roster, raw payment record, and interpretation rules from the workbook. Apply the following controls:

1. Treat PKR 45,000 as the expected total: 18 people at PKR 2,500 each.
2. Normalize case, punctuation, initials, nicknames, and short forms only where the supplied rules create a unique match.
3. Map “Sana Baji” to Sana Tariq and similar unique short forms to their roster names.
4. Split Umer F.'s PKR 5,000 transfer equally between Umer Farooq and Bilal Ahmed because the note says “self+bilal.”
5. Credit Mrs Osman Javed's transfer to Osman Javed because the note says it was on his behalf.
6. Treat the second same-day PKR 2,500 Hassan Sheikh transfer as a duplicate and do not apply it to dues.
7. Treat Mahnoor's PKR 1,500 as a partial payment and calculate the unpaid balance.
8. Do not assign the unregistered PKR 2,500 transfer to anyone.
9. Produce separate reports for matched payments, duplicates, unidentified transfers, and people needing follow-up.
10. Include a control proving that credited amounts plus duplicate amounts plus unidentified amounts equal the raw digital total.

## Final Refinement Prompt

Explain why a raw digital total above the expected total does not prove that everyone paid. Separate valid roster credits from duplicates and unidentified cash. Name each person requiring action and state the exact amount.
