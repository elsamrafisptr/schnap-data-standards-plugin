# SCHNAP `/py` Tooling Overview (Context for Data Requests)

This summarizes the existing `product-scraper` codebase so Claude understands
what downstream tools will consume the CSVs it produces. Read this when an
admin's request references pulling, pushing, enriching, or syncing product
data, so column choices and formats stay compatible with these scripts.

## Store architecture
- CS-Cart platform, two company entities: `oldy` (company_id 1, legacy) and
  `newly` (company_id 2, current). Product ID `80,000` is the common
  boundary heuristic between them.
- MySQL database `schnap_v2` holds the staging/working tables: `newly`,
  `oldy`, `brands`, `orders`, `master_list`, `category_map`, `cgpt`, plus
  many per-supplier scrape tables.

## Pipeline stages relevant to data prep
1. **Ingestion** (`pull.py`) — pulls from CS-Cart REST API into `newly`/`oldy`.
2. **Enrichment** (`cgpt.py`, `title_normalizer.py`, `_newly_dev` enhancer
   pipelines) — LLM-based title normalization (`[Product Type] [Specs]
   [Brand]`), SEO metadata, HTML spec sheets, dimension/weight inference.
3. **Reconciliation** (`price-check.py`, `compare_master_list.py`,
   `discontinued_checker.py`) — matches supplier data against
   `master_list` by SKU/product_code.
4. **Push back** (`push.py`, `push_v2.py`, `update_products_with_categories.py`,
   `update_price.py`) — writes changes back to CS-Cart via REST PUT, after a
   dirty-diff comparison to avoid redundant writes.

## Practical implications for data output
- Match by `product_code` (SKU) when joining supplier/master data to SCHNAP
  records — this is the convention used throughout the codebase, not
  `product_id` (which is CS-Cart-internal and only stable once a product
  already exists in the store).
- Prices: `list_price`, `price`, and `t3` (Tier 3 wholesale) are distinct
  fields — don't collapse them into one "price" column.
- Descriptions (`full_description`) are HTML, not plain text — if generating
  or updating this field, keep it valid HTML matching the existing section
  structure used by `cgpt.py` (Technical Specifications, Key Features,
  Installation Requirements, Standards & Compliance, Environmental Benefits,
  Warranty).
- `category_ids` / `category_names` and `brand_id` / `brand_name` are paired
  columns — if you populate one, populate its counterpart too when the
  mapping is known.

## CS-Cart API reference
For anything about specific CS-Cart REST endpoints, request/response shapes,
authentication, or object fields not covered above, consult the official
docs at https://docs.cs-cart.com/latest/ rather than guessing — CS-Cart's
API surface is large and version-specific.
