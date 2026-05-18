#!/usr/bin/env python3
"""Crunch all lead-like data files using a simple CRUNCG logic protocol.

CRUNCG protocol:
- C: Collect all CSV/XLS/XLSX files in repo root.
- R: Read files safely and normalize column names.
- U: Unify core lead fields (name, phone, email, source_file).
- N: Normalize phone digits and basic country code guess.
- C: Collapse duplicates by normalized phone, preferring richer rows.
- G: Generate outputs (consolidated CSV + JSON quality report).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT_CSV = ROOT / "crunched_all_cruncg.csv"
OUT_JSON = ROOT / "cruncg_quality_report.json"

NAME_KEYS = ["name", "full_name", "customer_name", "lead_name"]
PHONE_KEYS = ["phone", "mobile", "whatsapp", "contact", "phone_number"]
EMAIL_KEYS = ["email", "mail", "email_address"]


def norm_col(c: str) -> str:
    return "_".join(str(c).strip().lower().replace("-", " ").split())


def pick_col(cols: List[str], options: List[str]) -> str | None:
    for o in options:
        if o in cols:
            return o
    return None


def normalize_phone(v: object) -> str:
    digits = "".join(ch for ch in str(v) if ch.isdigit())
    if digits.startswith("00"):
        digits = digits[2:]
    if digits.startswith("0") and len(digits) == 10:
        digits = "971" + digits[1:]
    return digits


def country_code(phone: str) -> str:
    if phone.startswith("971"):
        return "971"
    if phone.startswith("86"):
        return "86"
    if phone.startswith("1") and len(phone) in {11}:
        return "1"
    return "unknown"


def read_file(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path, low_memory=False)
    return pd.read_excel(path)


def main() -> None:
    files = [
        p for p in ROOT.iterdir()
        if p.is_file() and p.suffix.lower() in {".csv", ".xlsx", ".xls"}
        and not p.name.startswith("~$")
    ]

    rows: List[Dict[str, object]] = []
    for f in files:
        try:
            df = read_file(f)
        except Exception:
            continue

        df = df.rename(columns={c: norm_col(c) for c in df.columns})
        cols = list(df.columns)
        name_col = pick_col(cols, NAME_KEYS)
        phone_col = pick_col(cols, PHONE_KEYS)
        email_col = pick_col(cols, EMAIL_KEYS)

        if not phone_col:
            continue

        local = pd.DataFrame()
        local["name"] = df[name_col] if name_col else ""
        local["phone_original"] = df[phone_col]
        local["email"] = df[email_col] if email_col else ""
        local["source_file"] = f.name

        for r in local.to_dict(orient="records"):
            r["phone_normalized"] = normalize_phone(r["phone_original"])
            r["phone_country_code"] = country_code(r["phone_normalized"])
            rows.append(r)

    out = pd.DataFrame(rows)
    if out.empty:
        raise SystemExit("No usable lead rows found.")

    out["completeness_score"] = (
        out[["name", "email"]].fillna("").astype(str).applymap(lambda x: 1 if x.strip() else 0).sum(axis=1)
    )
    out = out.sort_values(["phone_normalized", "completeness_score"], ascending=[True, False])
    dedup = out.drop_duplicates(subset=["phone_normalized"], keep="first").drop(columns=["completeness_score"])
    dedup.to_csv(OUT_CSV, index=False)

    report = {
        "total_rows_ingested": int(len(out)),
        "unique_leads_after_dedup": int(len(dedup)),
        "duplicate_rows_removed": int(len(out) - len(dedup)),
        "invalid_phone_rows": int((dedup["phone_normalized"].str.len() < 8).sum()),
        "country_code_breakdown": dedup["phone_country_code"].value_counts().to_dict(),
    }
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV.name} and {OUT_JSON.name}")


if __name__ == "__main__":
    main()
