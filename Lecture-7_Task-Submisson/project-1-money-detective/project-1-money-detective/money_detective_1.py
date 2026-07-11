#!/usr/bin/env python3
"""
Money Detective
Analyzes a CSV bank statement for:
- recurring/contract-like charges
- exact and possible duplicate payments
- repeated merchants and spending patterns
- monthly totals and balance reconciliation

Usage:
    python money_detective.py bank_statement.csv
    python money_detective.py bank_statement.csv --output-dir results
"""

from __future__ import annotations

import argparse
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable

import pandas as pd


RECURRING_KEYWORDS = {
    "subscription", "membership", "internet", "fibre", "mobile",
    "electricity", "bill payment", "insurance", "software", "cloud",
    "hosting", "service charges"
}

GENERIC_WORDS = {
    "pos", "purchase", "payment", "bank", "transfer", "atm",
    "withdrawal", "order", "bill", "online", "card"
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find possible money leaks in a bank statement.")
    parser.add_argument("csv_file", type=Path, help="CSV containing date, description and amount")
    parser.add_argument(
        "--output-dir", type=Path, default=Path("results"),
        help="Folder for generated CSV and text reports"
    )
    parser.add_argument(
        "--duplicate-days", type=int, default=3,
        help="Maximum day gap for possible duplicate payments"
    )
    return parser.parse_args()


def locate_column(columns: Iterable[str], candidates: Iterable[str]) -> str:
    normalized = {re.sub(r"[^a-z0-9]", "", c.lower()): c for c in columns}
    for candidate in candidates:
        key = re.sub(r"[^a-z0-9]", "", candidate.lower())
        if key in normalized:
            return normalized[key]

    for c in columns:
        low = c.lower()
        if any(candidate.lower() in low for candidate in candidates):
            return c

    raise ValueError(f"Could not find any of these columns: {', '.join(candidates)}")


def normalize_description(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    words = [w for w in text.split() if w not in GENERIC_WORDS]
    return " ".join(words)


def merchant_name(description: str) -> str:
    raw = str(description).strip()
    low = raw.lower()

    # Transaction-type descriptions need different parsing rules.
    if low.startswith("careem"):
        return "Careem"
    if low.startswith("pos purchase") and "-" in raw:
        return raw.split("-", 1)[1].strip().split(",")[0]
    if low.startswith("gym membership") and "-" in raw:
        return raw.split("-", 1)[1].strip()
    if low.startswith("internet bill") and "-" in raw:
        return raw.split("-", 1)[1].strip()
    if low.startswith("mobile top-up") and "-" in raw:
        return raw.split("-", 1)[1].strip()
    if "subscription" in low:
        return raw.replace("Subscription", "").strip()
    if "service charges" in low:
        return "Bank Service Charges"

    cleaned = normalize_description(raw)
    return cleaned or raw


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.csv_file)
    date_col = locate_column(df.columns, ["date", "transaction date"])
    desc_col = locate_column(df.columns, ["description", "details", "narration"])
    amount_col = locate_column(df.columns, ["amount", "transaction amount"])

    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce")
    df = df.dropna(subset=[date_col]).sort_values(date_col).reset_index(drop=True)
    df["normalized_description"] = df[desc_col].map(normalize_description)
    df["merchant"] = df[desc_col].map(merchant_name)
    df["is_expense"] = df[amount_col] < 0
    df["expense"] = df[amount_col].where(df["is_expense"], 0).abs()
    df["income"] = df[amount_col].where(df[amount_col] > 0, 0)

    # Opening balance rows normally have a blank amount.
    tx = df[df[amount_col].notna()].copy()
    expenses = tx[tx["is_expense"]].copy()

    total_inflows = tx["income"].sum()
    total_outflows = tx["expense"].sum()
    net_movement = tx[amount_col].sum()

    # Exact duplicate: same date, same absolute amount, same normalized description.
    exact_mask = expenses.duplicated(
        subset=[date_col, amount_col, "normalized_description"], keep=False
    )
    exact_duplicates = expenses[exact_mask].copy()

    # Possible duplicates: same amount, close dates and similar descriptions.
    possible_rows = []
    expense_records = expenses.reset_index().to_dict("records")
    for i, left in enumerate(expense_records):
        for right in expense_records[i + 1:]:
            if abs(left[amount_col] - right[amount_col]) > 0.01:
                continue
            day_gap = abs((left[date_col] - right[date_col]).days)
            desc_similarity = similarity(
                left["normalized_description"], right["normalized_description"]
            )
            if day_gap <= args.duplicate_days and desc_similarity >= 0.70:
                possible_rows.append({
                    "date_1": left[date_col].date(),
                    "description_1": left[desc_col],
                    "date_2": right[date_col].date(),
                    "description_2": right[desc_col],
                    "amount": abs(left[amount_col]),
                    "day_gap": day_gap,
                    "description_similarity": round(desc_similarity, 2),
                })
    possible_duplicates = pd.DataFrame(possible_rows)

    # Recurring/contract-like charges: keywords plus merchants repeated in the data.
    recurring_keyword_pattern = "|".join(re.escape(k) for k in RECURRING_KEYWORDS)
    keyword_recurring = expenses[
        expenses[desc_col].str.lower().str.contains(
            recurring_keyword_pattern, regex=True, na=False
        )
    ].copy()

    repeated_merchants = (
        expenses.groupby("merchant", dropna=False)
        .agg(
            payment_count=(amount_col, "size"),
            total_spend=("expense", "sum"),
            average_payment=("expense", "mean"),
            first_date=(date_col, "min"),
            last_date=(date_col, "max"),
        )
        .query("payment_count >= 2")
        .sort_values(["payment_count", "total_spend"], ascending=[False, False])
        .reset_index()
    )

    recurring_candidates = keyword_recurring[
        [date_col, desc_col, amount_col, "merchant", "expense"]
    ].sort_values("expense", ascending=False)

    # Category summary when a category column exists.
    category_col = None
    try:
        category_col = locate_column(df.columns, ["category"])
    except ValueError:
        pass

    if category_col:
        category_summary = (
            tx.groupby(category_col)
            .agg(
                transaction_count=(amount_col, "size"),
                inflows=("income", "sum"),
                outflows=("expense", "sum"),
                net=(amount_col, "sum"),
            )
            .sort_values("outflows", ascending=False)
            .reset_index()
        )
    else:
        category_summary = pd.DataFrame()

    # Balance reconciliation when a balance column exists.
    reconciliation_text = "Balance reconciliation not available."
    balance_difference = None
    try:
        balance_col = locate_column(df.columns, ["balance", "closing balance"])
        opening_balance = pd.to_numeric(df[balance_col], errors="coerce").dropna().iloc[0]
        closing_balance = pd.to_numeric(df[balance_col], errors="coerce").dropna().iloc[-1]
        expected_closing = opening_balance + net_movement
        balance_difference = closing_balance - expected_closing
        reconciliation_text = (
            f"Opening balance: {opening_balance:,.2f}\n"
            f"Closing balance: {closing_balance:,.2f}\n"
            f"Net transaction movement: {net_movement:,.2f}\n"
            f"Expected closing balance: {expected_closing:,.2f}\n"
            f"Reconciliation difference: {balance_difference:,.2f}"
        )
    except (ValueError, IndexError):
        pass

    recurring_total = recurring_candidates["expense"].sum()
    repeated_total = repeated_merchants["total_spend"].sum() if not repeated_merchants.empty else 0

    summary = f"""MONEY DETECTIVE REPORT
======================

Period: {df[date_col].min().date()} to {df[date_col].max().date()}
Transactions analyzed: {len(tx)}

VERIFIED TOTALS
---------------
Total inflows: {total_inflows:,.2f}
Total outflows: {total_outflows:,.2f}
Net movement: {net_movement:,.2f}

{reconciliation_text}

LEAK CHECKS
-----------
Recurring/contract-like charges found: {len(recurring_candidates)}
Recurring/contract-like total: {recurring_total:,.2f}
Exact duplicate rows found: {len(exact_duplicates)}
Possible duplicate pairs found: {len(possible_duplicates)}
Repeated merchants found: {len(repeated_merchants)}

INTERPRETATION
--------------
A recurring candidate is not automatically wasteful. It is a review list.
A possible duplicate is not automatically an error. Confirm it against receipts or the bank app.
"""

    (args.output_dir / "summary.txt").write_text(summary, encoding="utf-8")
    recurring_candidates.to_csv(args.output_dir / "recurring_candidates.csv", index=False)
    exact_duplicates.to_csv(args.output_dir / "exact_duplicates.csv", index=False)
    possible_duplicates.to_csv(args.output_dir / "possible_duplicates.csv", index=False)
    repeated_merchants.to_csv(args.output_dir / "repeated_merchants.csv", index=False)
    if not category_summary.empty:
        category_summary.to_csv(args.output_dir / "category_summary.csv", index=False)

    print(summary)
    if not recurring_candidates.empty:
        print("\nRECURRING / CONTRACT-LIKE REVIEW LIST")
        print(recurring_candidates[[date_col, desc_col, "expense"]].to_string(index=False))
    if not repeated_merchants.empty:
        print("\nREPEATED MERCHANTS")
        print(repeated_merchants.to_string(index=False))


if __name__ == "__main__":
    main()
