#!/usr/bin/env python3
"""
validate_csv.py — Check a generated product CSV against the SCHNAP
canonical newly/oldy schema and the plugin's house-style rules.

Usage:
    python validate_csv.py path/to/output.csv
    python validate_csv.py path/to/output.csv --strict   (fail on extra columns too)

Exit code 0 = pass, 1 = violations found. Prints a human-readable report
either way so Claude (or the admin) can see exactly what to fix.
"""

import csv
import re
import sys
import argparse

# Canonical column order from references/database_schema.md.
CANONICAL_COLUMNS = [
    "product_id", "min_items_in_box", "max_items_in_box", "box_length",
    "box_width", "box_height", "product_code", "product_type", "status",
    "company_id", "list_price", "amount", "weight", "length", "width",
    "height", "shipping_freight", "low_avail_limit", "timestamp",
    "updated_timestamp", "usergroup_ids", "is_edp", "edp_shipping",
    "unlimited_download", "tracking", "free_shipping", "zero_price_action",
    "is_pbp", "is_op", "is_oper", "is_returnable", "return_period",
    "avail_since", "out_of_stock_actions", "localization", "min_qty",
    "max_qty", "qty_step", "list_qty_count", "tax_ids", "age_verification",
    "age_limit", "options_type", "exceptions_type", "details_layout",
    "shipping_params", "facebook_obj_type", "parent_product_id",
    "buy_now_url", "units_in_product", "show_price_per_x_units",
    "algolia_object_id", "algolia_sync_status", "lang_code", "product",
    "shortname", "short_description", "full_description", "meta_keywords",
    "meta_description", "search_words", "page_title", "age_warning_message",
    "promo_text", "unit_name", "price", "category_ids", "popularity",
    "company_name", "sales_amount", "seo_name", "seo_path",
    "discussion_type", "average_rating", "product_reviews_count",
    "category_names", "base_price", "main_category", "image_pairs",
    "main_pair", "product_features", "options_type_raw",
    "exceptions_type_raw", "tracking_raw", "zero_price_action_raw",
    "min_qty_raw", "max_qty_raw", "qty_step_raw", "list_qty_count_raw",
    "details_layout_raw", "detailed_params", "relative_vendor_rating",
    "premoderation_reason", "have_required", "brand_id", "brand_name",
    "suplier_id", "t3", "batch_timestamp",
]
CANONICAL_SET = set(CANONICAL_COLUMNS)

SNAKE_CASE_RE = re.compile(r"^[a-z0-9]+(_[a-z0-9]+)*$")

# SEO field length guidance (see references/seo_rules.md)
SEO_LIMITS = {
    "page_title": (1, 60),
    "meta_description": (140, 160),
}


def check_headers(headers, strict):
    issues = []

    if not headers:
        issues.append("ERROR: CSV has no header row.")
        return issues

    # Rule: product_id must be first.
    if headers[0] != "product_id":
        issues.append(
            f"ERROR: First column is '{headers[0]}', must be 'product_id'."
        )
    elif "product_id" not in headers:
        issues.append("ERROR: 'product_id' column is missing entirely.")

    # Rule: snake_case.
    for h in headers:
        if not SNAKE_CASE_RE.match(h):
            issues.append(f"ERROR: Column '{h}' is not snake_case.")

    # Rule: prefer canonical names; flag unknowns.
    extras = [h for h in headers if h not in CANONICAL_SET]
    if extras:
        level = "ERROR" if strict else "WARNING"
        issues.append(
            f"{level}: Column(s) not in canonical schema (ok if intentional "
            f"new field, but flag to admin): {', '.join(extras)}"
        )

    # Duplicate headers.
    seen = set()
    dupes = set()
    for h in headers:
        if h in seen:
            dupes.add(h)
        seen.add(h)
    if dupes:
        issues.append(f"ERROR: Duplicate column name(s): {', '.join(dupes)}")

    return issues


def check_rows(headers, rows):
    issues = []
    id_idx = headers.index("product_id") if "product_id" in headers else None

    seen_ids = set()
    for i, row in enumerate(rows, start=2):  # row 1 is header
        if id_idx is not None:
            pid = row[id_idx].strip() if id_idx < len(row) else ""
            if not pid:
                issues.append(f"ERROR: Row {i} has empty product_id.")
            elif pid in seen_ids:
                issues.append(f"ERROR: Row {i} has duplicate product_id '{pid}'.")
            else:
                seen_ids.add(pid)

        for field, (min_len, max_len) in SEO_LIMITS.items():
            if field in headers:
                val = row[headers.index(field)] if headers.index(field) < len(row) else ""
                length = len(val)
                if val and not (min_len <= length <= max_len):
                    issues.append(
                        f"WARNING: Row {i} '{field}' is {length} chars "
                        f"(recommended {min_len}-{max_len})."
                    )
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path")
    parser.add_argument(
        "--strict", action="store_true",
        help="Treat non-canonical extra columns as errors, not warnings."
    )
    args = parser.parse_args()

    with open(args.csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        print("ERROR: CSV file is empty.")
        sys.exit(1)

    headers, data_rows = rows[0], rows[1:]

    issues = check_headers(headers, args.strict)
    issues += check_rows(headers, data_rows)

    errors = [i for i in issues if i.startswith("ERROR")]
    warnings = [i for i in issues if i.startswith("WARNING")]

    print(f"Validated: {args.csv_path}")
    print(f"Columns: {len(headers)} | Rows: {len(data_rows)}")
    print()
    if not issues:
        print("PASS: no issues found.")
        sys.exit(0)

    if errors:
        print(f"{len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  - {w}")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
