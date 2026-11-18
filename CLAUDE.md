# PAP Partners

- A directory of the partners PAP works with: ODMs and suppliers, logistics (hub, HSN Group) and the service network (NS, ASP).
- `index.html` is the whole site. It reads `data/odm.json` and `data/partners.json`; nothing is hard-coded in the page.
- `data/odm.json` is **generated**: `python3 tools/build_odm.py path/to/AAP_Critical_Report_YYYYMMDDhhmmss.csv`.
  Never edit it by hand and never commit the CSV (it is in `.gitignore`).
- `data/partners.json` is kept by hand: logistics and service entries, plus `supplierNotes` (notes, contacts, full names) keyed by the supplier name in `odm.json`.
- Only write facts that come from Sandy, her Acer Guide or the Critical Report, and name the source. Don't invent full names, countries or descriptions.
- Names, codes, system names and units stay English. The page is English only.
- The site sits behind Basic Auth in `middleware.js` (same login as Acer Guide). Partner details are confidential: keep the repo private.
- Design follows Acer Guide: brown / amber, Patrick Hand, panels with a dark border and shadow.
