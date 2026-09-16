# schnap-data-standards

A Claude plugin that standardizes how admins use Claude for SCHNAP
(schnap.com.au) product/catalog data work — data science, cleanup,
enrichment, and exports.

## What it does

When installed, Claude will automatically:
- Output tabular product data as **CSV**, with `product_id` as the first
  column and all headers in `snake_case`.
- Map any data onto the canonical `newly`/`oldy` MySQL schema (see
  `skills/schnap-data-standards/references/database_schema.md`) instead of
  inventing new column names.
- Apply SCHNAP's SEO conventions for electrical products (title format,
  meta length, slugs, description structure) — see
  `skills/schnap-data-standards/references/seo_rules.md`.
- Stay compatible with the existing `/py` scraping/enrichment/CS-Cart-push
  pipeline (join keys, HTML description structure, price field usage) — see
  `skills/schnap-data-standards/references/tooling_overview.md`.
- Point to https://docs.cs-cart.com/latest/ for anything CS-Cart-API-specific
  it isn't already told.

These rules apply *on top of* whatever an admin's own prompt asks for — they
never override the actual task, just the formatting/standards around it.

## Installation

In Claude Code / Claude Desktop, add this repo as a plugin source and enable
`schnap-data-standards`, or point your team's plugin catalog at this GitHub
repo directly.

## Structure

```
.claude-plugin/
  plugin.json                     # plugin manifest
skills/
  schnap-data-standards/
    SKILL.md                      # core rules Claude follows
    references/
      database_schema.md          # canonical newly/oldy column list
      seo_rules.md                # electrical-product SEO conventions
      tooling_overview.md         # how this fits the /py pipeline
    scripts/
      validate_csv.py             # validates a generated CSV against the schema/rules
```

## Validator script

`scripts/validate_csv.py` checks a generated CSV against the canonical
schema and house-style rules: `product_id` first, snake_case headers, no
duplicate/empty `product_id`s, columns matched against the canonical list,
and SEO field length checks (`page_title`, `meta_description`). Claude runs
this automatically before delivering any CSV; you can also run it by hand:

```bash
python3 skills/schnap-data-standards/scripts/validate_csv.py path/to/file.csv
python3 skills/schnap-data-standards/scripts/validate_csv.py path/to/file.csv --strict
```

Exit code `0` = pass (warnings allowed), `1` = errors found.

## Updating

- **Schema changes**: edit `database_schema.md` when columns are added/
  changed in the live `newly`/`oldy` tables.
- **SEO rules**: edit `seo_rules.md` as SCHNAP's SEO conventions evolve.
- **Pipeline changes**: edit `tooling_overview.md` if scripts in `/py`
  change join keys, field usage, or description structure.

Keep `SKILL.md` itself short — it should stay a pointer to these reference
files plus the four core formatting rules, not grow into a full spec.
