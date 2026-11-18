# PAP Partners

- A directory of the partners PAP works with: ODMs and suppliers, logistics (hub, HSN Group) and the service network (NS, ASP).
- `index.html` is the whole site. It reads `data/odm.json`, `data/partners.json` and `data/profiles.json`; no partner data is hard-coded in the page.
- The site has two complete languages, switched by the EN · 中文 button (`?lang=zh`, remembered in localStorage). Never mix them: every
  text field in the data is `{en, zh}`, and every page label lives in `UI.en` / `UI.zh` in the script. Names, codes, system names and
  product-line codes stay English in both.
- `data/odm.json` is **generated**: `python3 tools/build_odm.py path/to/AAP_Critical_Report_YYYYMMDDhhmmss.csv`.
  Never edit it by hand and never commit the CSV (it is in `.gitignore`).
- "What they do for PAP" for a supplier is written by the page from its product lines and part categories (`FAMILIES`, `CATS`).
- `data/profiles.json`: one short company description per supplier name, in both languages, with its source. Add one only when a
  source confirms it; otherwise leave the supplier out.
- `data/partners.json` is kept by hand: logistics and service entries, plus `supplierNotes` (facts, notes, full names) keyed by the supplier name.
- Don't add contacts: no people's names, email addresses or mail recipients (Sandy's rule, Nov 2026).
- Only write facts that come from Sandy, her Acer Guide, the Critical Report or a named public source. Don't invent full names, countries or descriptions.
- The site sits behind Basic Auth in `middleware.js` (same login as Acer Guide). Partner details are confidential: keep the repo private.
- Design follows Acer Guide: brown / amber, Patrick Hand, panels with a dark border and shadow.
