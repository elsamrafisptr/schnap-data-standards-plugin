---
name: schnap-data-standards
description: Standardizes any data science, catalog cleanup, enrichment, export, or product-data task for SCHNAP (schnap.com.au), an electrical products CS-Cart store. Always use this skill whenever an admin asks Claude to produce, transform, clean, enrich, or export SCHNAP product/catalog data — including requests that just say "format this", "clean this list", "generate SEO for these products", or paste a spreadsheet/CSV of products — even if they don't explicitly mention SCHNAP, CS-Cart, or "standards". Enforces CSV output mapped to the canonical newly/oldy database schema, snake_case columns, product_id first, and SCHNAP's SEO conventions for electrical products.
---

# SCHNAP Data Standards

This skill makes Claude's output consistent no matter which admin is asking
or how they phrase the request. It is a standing house style for SCHNAP
product/catalog data work — apply it on top of whatever the admin's prompt
asks for, never instead of it.

## When this applies

Any task that produces, edits, or exports rows of SCHNAP product data:
cleaning a scraped supplier list, generating SEO copy, reconciling a master
list, preparing an upload file, summarizing a catalog extract, etc. If the
admin's request and this skill conflict on *what* to do (e.g. "just give me
the top 10 by price"), do that task — but still apply the formatting rules
below to any tabular data you output.

## Core formatting rules (non-negotiable)

1. **Always output CSV.** Even if the admin didn't ask for a file format
   explicitly, tabular product data goes out as CSV — not JSON, not a
   markdown table, unless the admin explicitly asks for a different format
   for that one request.
2. **Always conform to the canonical database structure.** See
   `references/database_schema.md` for the full `newly`/`oldy` column list,
   types, and mapping guidance. Don't invent alternate names for concepts
   already covered by that schema.
3. **`product_id` is always the first column.** No exceptions — even if the
   source data has it elsewhere or omits it (in which case, ask the admin
   for it or leave it blank/flagged rather than reordering around its
   absence).
4. **All column names are snake_case.** `list_price` not `List Price` or
   `listPrice`; new columns not in the canonical schema must also be
   snake_case.

Before delivering any CSV, do a final self-check: is `product_id` column 1?
Is every header snake_case? Does every column that has a canonical
counterpart use that exact name? Is the output actually a CSV file/block,
not a markdown table?

### Automated validation

After writing the CSV to disk, always run it through the bundled validator
before presenting it to the admin:

```bash
python3 scripts/validate_csv.py path/to/output.csv
```

Fix any reported `ERROR` lines and regenerate before delivering the file.
`WARNING` lines (e.g. a non-canonical extra column, or an SEO field outside
its recommended length) don't block delivery, but mention them to the admin
in your reply so nothing slips through silently. Use `--strict` if the admin
asks for zero tolerance on extra/unknown columns.

## SEO rules for electrical product data

When the task touches product titles, meta fields, slugs, or descriptions,
follow `references/seo_rules.md` — SCHNAP-specific title format
(`[Product Type] [Key Spec] [Brand]`), meta length limits, slug conventions,
and description structure for electrical products.

## Tooling & CS-Cart context

`references/tooling_overview.md` explains the existing `/py` pipeline
(scraping → enrichment → push to CS-Cart) so column choices, join keys
(match by `product_code`, not `product_id`, when reconciling supplier data),
and description formatting stay compatible with what the admin's scripts
expect downstream.

For anything about CS-Cart REST API specifics (endpoints, auth, object
fields) not already covered in the references, check
https://docs.cs-cart.com/latest/ rather than guessing.

## Working with the admin's own prompt

The admin will usually give a specific instruction on top of this skill
(e.g. "normalize these 200 titles", "flag discontinued SKUs", "generate
meta descriptions for this batch"). Always:
- Do exactly what they asked, except the standarization itself.
- Apply the four core formatting rules to any tabular output regardless.
- Apply the SEO rules when the output includes SEO-relevant fields.
- If their instruction would violate a core rule (e.g. "give me this as
  JSON with camelCase keys"), do what they explicitly asked for that
  request, but mention briefly that it deviates from the standard CSV/
  snake_case convention, so it's a visible choice, not silent drift.
