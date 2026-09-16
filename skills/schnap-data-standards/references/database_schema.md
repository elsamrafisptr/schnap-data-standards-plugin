# Canonical Product Table Schema (`newly` / `oldy`)

This is the authoritative column list and order for the SCHNAP product tables
in MySQL (`schnap_v2`). Both `newly` (company_id = 2) and `oldy`
(company_id = 1) share this schema.

Every CSV Claude produces for product data **must** map onto these columns —
same names, same snake_case, and `product_id` always first. Do not invent new
column names for concepts already covered here; do not silently drop columns
that were present in the source data.

| # | Column | Type | Nullable | Notes |
|---|--------|------|----------|-------|
| 1 | product_id | int | No | Primary key |
| 2 | min_items_in_box | int | Yes | |
| 3 | max_items_in_box | int | Yes | |
| 4 | box_length | int | Yes | |
| 5 | box_width | int | Yes | |
| 6 | box_height | int | Yes | |
| 7 | product_code | varchar(255) | Yes | SKU |
| 8 | product_type | varchar(10) | Yes | |
| 9 | status | varchar(10) | Yes | e.g. A = active |
| 10 | company_id | varchar(10) | Yes | 1 = oldy, 2 = newly |
| 11 | list_price | float | Yes | |
| 12 | amount | int | Yes | stock quantity |
| 13 | weight | float | Yes | |
| 14 | length | float | Yes | |
| 15 | width | float | Yes | |
| 16 | height | float | Yes | |
| 17 | shipping_freight | float | Yes | |
| 18 | low_avail_limit | int | Yes | |
| 19 | timestamp | int | Yes | created (unix) |
| 20 | updated_timestamp | int | Yes | updated (unix) |
| 21 | usergroup_ids | varchar(255) | Yes | |
| 22 | is_edp | varchar(10) | Yes | |
| 23 | edp_shipping | varchar(10) | Yes | |
| 24 | unlimited_download | varchar(10) | Yes | |
| 25 | tracking | varchar(10) | Yes | |
| 26 | free_shipping | varchar(10) | Yes | |
| 27 | zero_price_action | varchar(10) | Yes | |
| 28 | is_pbp | varchar(10) | Yes | |
| 29 | is_op | varchar(10) | Yes | |
| 30 | is_oper | varchar(10) | Yes | |
| 31 | is_returnable | varchar(10) | Yes | |
| 32 | return_period | int | Yes | |
| 33 | avail_since | int | Yes | |
| 34 | out_of_stock_actions | varchar(10) | Yes | |
| 35 | localization | text | Yes | |
| 36 | min_qty | int | Yes | |
| 37 | max_qty | int | Yes | |
| 38 | qty_step | int | Yes | |
| 39 | list_qty_count | int | Yes | |
| 40 | tax_ids | longtext | Yes | |
| 41 | age_verification | varchar(10) | Yes | |
| 42 | age_limit | int | Yes | |
| 43 | options_type | varchar(10) | Yes | |
| 44 | exceptions_type | varchar(10) | Yes | |
| 45 | details_layout | varchar(255) | Yes | |
| 46 | shipping_params | longtext | Yes | |
| 47 | facebook_obj_type | varchar(255) | Yes | |
| 48 | parent_product_id | varchar(255) | Yes | |
| 49 | buy_now_url | text | Yes | |
| 50 | units_in_product | float | Yes | |
| 51 | show_price_per_x_units | float | Yes | |
| 52 | algolia_object_id | varchar(255) | Yes | |
| 53 | algolia_sync_status | varchar(255) | Yes | |
| 54 | lang_code | varchar(10) | Yes | |
| 55 | product | text | Yes | product title |
| 56 | shortname | text | Yes | |
| 57 | short_description | longtext | Yes | |
| 58 | full_description | longtext | Yes | HTML |
| 59 | meta_keywords | longtext | Yes | |
| 60 | meta_description | longtext | Yes | |
| 61 | search_words | text | Yes | |
| 62 | page_title | text | Yes | SEO title |
| 63 | age_warning_message | text | Yes | |
| 64 | promo_text | text | Yes | |
| 65 | unit_name | varchar(255) | Yes | |
| 66 | price | float | Yes | |
| 67 | category_ids | longtext | Yes | |
| 68 | popularity | varchar(255) | Yes | |
| 69 | company_name | varchar(255) | Yes | |
| 70 | sales_amount | varchar(255) | Yes | |
| 71 | seo_name | text | Yes | SEO slug |
| 72 | seo_path | text | Yes | |
| 73 | discussion_type | varchar(10) | Yes | |
| 74 | average_rating | float | Yes | |
| 75 | product_reviews_count | int | Yes | |
| 76 | category_names | text | Yes | |
| 77 | base_price | float | Yes | |
| 78 | main_category | int | Yes | |
| 79 | image_pairs | longtext | Yes | |
| 80 | main_pair | longtext | Yes | |
| 81 | product_features | longtext | Yes | PHP-serialized |
| 82 | options_type_raw | varchar(10) | Yes | |
| 83 | exceptions_type_raw | varchar(10) | Yes | |
| 84 | tracking_raw | varchar(10) | Yes | |
| 85 | zero_price_action_raw | varchar(10) | Yes | |
| 86 | min_qty_raw | varchar(10) | Yes | |
| 87 | max_qty_raw | varchar(10) | Yes | |
| 88 | qty_step_raw | varchar(10) | Yes | |
| 89 | list_qty_count_raw | varchar(10) | Yes | |
| 90 | details_layout_raw | varchar(255) | Yes | |
| 91 | detailed_params | longtext | Yes | PHP-serialized |
| 92 | relative_vendor_rating | int | Yes | |
| 93 | premoderation_reason | text | Yes | |
| 94 | have_required | varchar(10) | Yes | |
| 95 | brand_id | int | Yes | |
| 96 | brand_name | varchar(255) | Yes | |
| 97 | suplier_id | int | Yes | |
| 98 | t3 | float | Yes | Tier 3 wholesale price |
| 99 | batch_timestamp | int | Yes | |

## Rules for mapping ad-hoc/enriched data onto this schema

- If the admin's data has an equivalent concept (e.g. "title" / "name"), map
  it to the matching canonical column (`product` for title, `seo_name` /
  `seo_path` for slugs, `full_description` for HTML description, etc.)
  instead of creating a new column.
- If a column genuinely doesn't exist in this schema (e.g. a new AI-derived
  field like `ai_confidence_score`), it's fine to append it as an *extra*
  trailing column — but never rename or replace a canonical column to do so,
  and flag the new column explicitly in your response so the admin notices it.
- Preserve `product_id` values exactly as given; never regenerate or guess
  IDs.
