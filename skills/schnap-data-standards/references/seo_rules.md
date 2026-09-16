# SEO Rules for SCHNAP Electrical Products (schnap.com.au)

Apply these whenever generating or editing `product` (raw/display title),
`page_title` (SEO/meta title), `meta_description`, `meta_keywords`,
`seo_name`, `seo_path`, `short_description`, or `full_description` for
SCHNAP catalog data. Calibrated against SCHNAP's real enrichment output
(e.g. Pulset RCBO 1P 16A 10kA), so match this style, not a generic template.

## Two distinct titles — don't conflate them

- `product` (raw/internal title): can stay close to the source/scraped
  title, spec-forward (e.g. `RCBO 1P 16A 10kA Breaking Capacity Short
  Circuit Pulset`). This is what pulls in from suppliers and doesn't need
  to be SEO-perfect on its own.
- `page_title` (the actual customer/SEO-facing title, i.e. `meta_title` in
  AI-enrichment output): must be a clean, human-readable spec-led title,
  built in **spec → product type → sub-type/technology → product code**
  order, e.g.:
  `1 Pole 16Amp MCB/RCD 10KA Mechanical Combination AC Type - RCBO/1P16M`
  `LED Batten Light 20W 4000K - LED-BAT-20W-40K`
  - Lead with the distinguishing specs (poles/wattage/amps/rating), not the
    brand and not filler words ("premium", "high quality").
  - End with ` - [product_code]` when a clean SKU/code exists — this is the
    SCHNAP convention and helps exact-match searches.
  - Brand (`brand_name`) is its own field; only include it in `page_title`
    if it meaningfully disambiguates (rare) — don't default to appending it.
  - Keep to roughly 60 characters where possible; if a fully descriptive
    title runs longer (common for technical electrical specs), prioritize
    clarity and correctness over hard truncation.

## Meta description (`meta_description`)
- 140–160 characters.
- Summarize what the product *is* and its core value in plain language,
  matching this register: *"The Pulset 1 Pole 16Amp MCB/RCD 10KA Mechanical
  Combination provides reliable electrical protection with a compact
  design, ideal for both residential and commercial installations."*
- Include product type + one key spec + a use-case/benefit. Avoid a hard
  sales CTA ("Buy now!") — SCHNAP's existing copy is informational, not
  pushy.
- Must accurately reflect the product — no unverifiable superlatives, no
  invented certifications.

## Meta keywords (`meta_keywords`)
- Comma-separated, lowercase, 5–10 terms: product type, sub-type/technology,
  brand, key specs, and search synonyms. Pull synonyms from an
  `alternatively_known_as`-style field when available (e.g. an RCBO should
  also list "miniature circuit breaker", "combination MCB/RCD") since
  customers search by informal names as often as technical ones.

## SEO slug (`seo_name` / `seo_path`)
- Lowercase, hyphen-separated, derived from `page_title` (not the raw
  `product` field), no stop words, no special characters:
  `1-pole-16amp-mcb-rcd-10ka-mechanical-combination-ac-type`.

## Descriptions (`short_description`, `full_description`)

`short_description`: 1–2 plain sentences combining product type + top spec
+ one distinguishing feature, e.g. *"Pulset RCBO Breaking Capacity Short
Circuit Protection features 16A rated current, 10kA and AS/NZS 61009.
Combination MCB and RCD for enhanced safety."* No keyword stuffing.

`full_description`: valid HTML using SCHNAP's exact existing section
structure and CSS classes (`container` / `column` / `full-width` /
`section-title`), in this order:
1. **Technical Specifications** — bullet list, `Label: value` pairs (rated
   current, type, capacity, poles, standards compliance, dimensions,
   weight, etc. — whatever applies to the product category).
2. **Key Features** — short benefit-oriented bullets.
3. **Professional Installation Requirements** — note licensed-electrician
   requirement where applicable to the product category (switchgear,
   wiring, circuit protection); omit for products that don't need
   installation (e.g. hand tools).
4. **Applications** — Residential / Commercial / Industrial bullets, only
   where genuinely applicable.
5. **Standards & Compliance** — cite the specific AS/NZS standard only if
   it's known/verified from source data; never fabricate a standard number.
   Leave the section out (don't guess) if unknown, and flag it to the admin.
6. **Environmental Benefits** — one or two bullets if there's a genuine
   efficiency/sustainability angle; omit rather than padding if there isn't.
7. **Warranty Information** — plain sentence, only the stated warranty term.
8. **Available Now** — one short paragraph restating the product and a
   plain (non-pushy) purchase/availability line — only if `status`/`amount`
   actually support it (see hygiene rule below).
9. A trailing `<div class="hidden pdata">{...}</div>` JSON blob mirroring
   the visible sections in structured form (`brand`, `weight_kg`,
   `meta_title`, `meta_description`, `applications`, `key_features`,
   `dimensions_mm`, `technical_specifications`,
   `australian_standards_compliance`, `professional_installation_requirements`,
   `warranty_information`, `alternatively_known_as`,
   `environmental_benefits`, `availability`). Keep this JSON in sync with
   the visible HTML above it — don't let them drift apart.

## General e-commerce SEO hygiene
- No duplicate `page_title`/slug across products — if a collision is likely
  (same type+brand, different pack size or rating), disambiguate with the
  distinguishing spec, not the brand.
- Never claim availability, stock, or pricing in SEO text (including the
  "Available Now" section) that isn't backed by the actual
  `amount`/`status`/`price` fields in the row — if a product is
  out-of-stock or discontinued, don't generate "available now" copy for it.
- Never fabricate an AS/NZS standard, certification, or warranty term that
  isn't present in the source data — flag it for admin review instead.
